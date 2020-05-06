# coding=utf-8
import time
import math
from pathlib import Path
from pprint import pprint

from utils import is_contains_chinese
from translate import baidu_translate


def translate_srt(path, appid, secretkey, from_lang='auto', to_lang='zh', is_premium=False, limit=950):
    '''
    翻譯一個 SRT 文件，生成文件後不會改動任何排版。
    可以改寫 translate() 函數接駁其他 API。
    translate() 返回一個字典，其中鍵'trans_result'為翻譯結果：
    {'trans_result': [{'src': '<原文1>', 'dst': '<譯文1>'}, {'src': '<原文2>', 'dst': '<譯文2>'}]}
    '''
    # 只需要有中文的行，才需要翻譯。
    to_translate_lines = get_chinese_lines(path)

    # 把句子合併成文章，減少請求次數。
    # 由於翻譯請求有字數限制，Get 1000字，Post 2000字。須統計總字數，以便之後分開若干部分翻譯。
    # 為免影響翻譯質量，以及之後重新寫入文件的難度。不能平均切割，須以句子方式，即逐行切割。
    text = ''.join(to_translate_lines)
    total_count = len(text)
    yield total_count

    to_translate_parts = []  # 裝載準備請求翻譯的部分文本。
    translations = []  # 裝載翻譯 API 返回結果。
    count = 0  # 計算循環當刻所讀取的字數。
    parts = 0  # 計算分成多少部分，即請求次數。
    for line in to_translate_lines:
        count += len(line)
        total_count -= len(line)
        # Get 請求不能超過 1000 字，這裏設限制在 950 字。
        # 文本不足 950 字只需發送一次請求，或者超過限制文本的最後一部分請求。
        if count < limit and total_count == 0:
            print(f'讀取字數 {count}, 剩餘字數{total_count}')
            to_translate_parts.append(line)

            # 發送請求。
            res = baidu_translate('\n'.join(to_translate_parts),
                                  appid,
                                  secretkey,
                                  from_lang=from_lang,
                                  to_lang=to_lang)
            print(res)
            translations += res.get('trans_result')

            parts += 1
            yield total_count
            print(f'This is part {parts}.')
            print(translations)

        # 每當檢測到即將超過 950 字，就將__此行文本之前__的部分本文發出請求。
        elif count >= limit and total_count > 0:
            print(f'讀取字數 {count}, 剩餘字數{total_count}')
            # 發送請求。
            res = baidu_translate('\n'.join(to_translate_parts),
                                  appid,
                                  secretkey,
                                  from_lang=from_lang,
                                  to_lang=to_lang)
            translations += res.get('trans_result')

            # 此行之前部分文本已翻譯。須清空待翻譯文本列表，再裝載這行文本。
            to_translate_parts = []
            to_translate_parts.append(line)

            count = 0
            parts += 1
            yield total_count
            print(f'This is part{parts}')
            print(translations)
            if is_premium:
                time.sleep(0.1)  # 高級版 API 權限為 10 QPS。
            else:
                time.sleep(1)  # 普通版 API 權限為 1 QPS。

        # 未檢測到超出 950 字前，將每行文本裝載入列表，準備發音。
        else:
            print('字數未超過限制，未發出請求。')
            to_translate_parts.append(line)

    # 最後返回翻譯文件的絕對路徑字符串。
    new_path = path.name.replace('.srt', f'_translated_{to_lang}.srt')
    new_path = new_path.replace('zh.srt', 'chs.srt')
    write_srt(new_path, path, translations)
    yield Path(new_path).absolute().__str__()


def get_chinese_lines(path):
    '''讀取srt文件，把有中文的行，即對白取出。'''
    with open(path) as file:
        lines = file.readlines()
        chinese_lines = []
        for line in lines:
            if is_contains_chinese(line):
                chinese_lines.append(line)
    return chinese_lines


def write_srt(new_path, old_path, translations):
    '''
    translations 是一個列表，每一項都是一個字典，每一個字典都有兩個鍵。具體如下：
    [{'src': '<原文1>', 'dst': '<譯文1>'}, {'src': '<原文2>', 'dst': '<譯文2>'}]
    '''
    with open(new_path, 'w') as n_file:
        with open(old_path) as o_file:
            lines = o_file.readlines()
            # 在原文中每一行，找到對應的文字，然後替換成譯文。
            # 請求結果 translations 是一個列表，每一項都是一個字典，每一個字典都有兩個鍵。具體如下：
            # [{'src': '<原文1>', 'dst': '<譯文1>'}, {'src': '<原文2>', 'dst': '<譯文2>'}]
            # 遍歷每一行，然後在字典中找到對應的原文，替換成譯文。
            # 之前寫過的一些用爬蟲的翻譯，由於獲得返回結果後沒有與原文生成一個字典的關係，因此後期排版難度大。
            copy_lines = lines.copy()
            for i, line in enumerate(lines):
                for td in translations:
                    source = td.get('src')
                    translation = td.get('dst')
                    if source == line.strip():
                        copy_lines[i] = translation + '\n'
            n_file.writelines(copy_lines)


if __name__ == '__main__':
    p = Path('sample.srt')
    trans_gen = translate_srt(p, from_lang='yue')
    total = trans_gen.send(None)
    print(f'需要翻譯：{total}字')
    for c in trans_gen:
        print(f'已翻譯 {c} 字')
