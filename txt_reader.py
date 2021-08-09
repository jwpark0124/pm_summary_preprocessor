# -*- coding: utf-8 -*-
"""txt_reader.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BJ-dboJw5bPPZHB90clQdUuoCnCzWw2U
"""

# !pip install hanja

import unicodedata
import hanja
import argparse
from hanja import hangul
import json
import re
from pprint import pprint
from glob import glob
import collections

sample = sorted(glob(
    "/Users/jaewanpark/Documents/회의록/pm_summary_preprocessor(pjw)/요약대상회의록-1차/*.txt"))
# pprint(sample)

# 파일 불러오기

# fname = "/content/drive/My Drive/Colab Notebooks/task/Minutes(Korean)/회의록 1차/284여성(예산결산기금심사)소위01.txt"
fname = "/Users/jaewanpark/Documents/회의록/pm_summary_preprocessor(pjw)/요약대상회의록-1차/311법사(법안심사제1)소위01(12.11.15).txt"
# fname = "/content/drive/My Drive/Colab Notebooks/task/Minutes(Korean)/회의록 1차/311환노(법안심사)소위01(12.9.17).txt"
# fname = "/content/drive/My Drive/Colab Notebooks/task/Minutes(Korean)/회의록 1차/320환노(예산결산기금심사)소위03(13.11.28).txt"
# fname = "/content/drive/My Drive/Colab Notebooks/task/Minutes(Korean)/회의록 1차/321교문(예산결산기금심사)소위03(13.12.16).txt"
# fname = "/content/drive/My Drive/Colab Notebooks/task/Minutes(Korean)/회의록 1차/321국토(교통법안심사)소위01(13.12.12).txt"
# fname = "/content/drive/My Drive/Colab Notebooks/task/Minutes(Korean)/회의록 1차/322국토(민투mrg대책)소위01(14.2.26).txt"
# fname = "/content/drive/My Drive/Colab Notebooks/task/Minutes(Korean)/회의록 1차/322국토(철도산업발전)소위01(14.2.7).txt"
# fname = "/content/drive/My Drive/Colab Notebooks/task/Minutes(Korean)/회의록 1차/323국토(철도산업발전)소위02(14.4.10).txt"
# fname = "/content/drive/My Drive/Colab Notebooks/task/Minutes(Korean)/회의록 1차/320교문(청원심사)소위01(13.11.18).txt"

# fname = "/content/drive/My Drive/Colab Notebooks/task/Minutes(Korean)/회의록 1차/346외통(법안심사)소위02(16.10.28.).txt"
# fname = "/content/drive/My Drive/Colab Notebooks/task/Minutes(Korean)/회의록 1차/347안행(안전및선거법심사)소위01(16.12.20.).txt"
# fname = "/content/drive/My Drive/Colab Notebooks/task/Minutes(Korean)/회의록 1차/354환노(고용노동)소위03(17.9.28.).txt"

# fname = "/content/drive/My Drive/Colab Notebooks/task/Minutes(Korean)/회의록 1차/337교문(예산결산기금심사)소위01(15.11.2).txt"

with open(fname, 'r', encoding='utf-8-sig') as file:
    txt = file.readlines()
    pass
# pprint(txt)


def clean_up(txt):
    tt = []
    text = []
    for page in txt:
        sent = page.strip()
        sent = sent.split("\n")
        tt += sent

    for han in range(len(tt)):
        ktext = tt[han].replace('臨', '임').replace("委", "위").replace("員", '원').replace("金", "김").replace("金", "김").replace('淇', '기').replace('春', '춘').replace("柳", "유").replace("李", "이").replace(
            "梁", "양").replace("羅", "나").replace("利", "이").replace("勞", "노").replace("樂", "락").replace("盧", "노").replace("樂", "락").replace("龍", "용").replace("沈", "심").replace("呂", "려").replace("寧", "영")
        text.append(ktext)
    return text


text = clean_up(txt)
# pprint(text)


def clean_up_or(txt):
    text_or = []
    # 모든페이지 다 나눠서 리스트에 넣기
    for page in txt:
        sent = page.strip()
        sent = sent.split("\n")
        text_or += sent
    return text_or


text_or = clean_up_or(txt)
# pprint(text_or)

# date 텍스트 파일에서 yyyymmdd 형태의 날짜 뽑기


def date_extractor(text):
    pm_date = ''
    for i in range(7, 11):
        # pm_d += text[i]
        # pm_da = pm_d.split(' ')
        if text[i].startswith("日"):
            pm_da = text[i].split(' ')
            pm_dat = pm_da[-1].split("年")
            year = pm_dat[0]
            # print(year)
            mmdd = pm_dat[1].split("(")
            md = mmdd[0]
            # print(len(md))
            for i in range(len(md[1])):
                if md[1] == "月":
                    month = "0" + md[0]
                    if md[3] == "日":
                        day = "0" + md[2]
                    elif md[4] == "日":
                        day = md[2] + md[3]
                elif md[2] == "月":
                    month = md[0] + md[1]
                    if md[4] == "日":
                        day = "0" + md[3]
                    elif md[5] == "日":
                        day = md[3] + md[4]
            date = year + month + day
        elif text[i].startswith("일"):
            pm_da = text[i].split(' ')
            pm_dat = pm_da[-1].split("년")
            year = pm_dat[0]
            # print(year)
            mmdd = pm_dat[1].split("(")
            md = mmdd[0]
            # print(len(md))
            for i in range(len(md[1])):
                if md[1] == "월":
                    month = "0" + md[0]
                    if md[3] == "일":
                        day = "0" + md[2]
                    elif md[4] == "일":
                        day = md[2] + md[3]
                elif md[2] == "월":
                    month = md[0] + md[1]
                    if md[4] == "일":
                        day = "0" + md[3]
                    elif md[5] == "일":
                        day = md[3] + md[4]
            date = year + month + day
    return date


pm_date = date_extractor(text)
# print(pm_date)

# 작성자


def author(text):
    pm_author = ''
    for i in range(6, 12):
        if text[i].startswith('國') and text[i].endswith('處') or text[i].startswith('국') and text[i].endswith('처'):
            pm_author = hanja.translate(
                ''.join(text[i].split(' ')), "substitution")
    return pm_author


pm_author = author(text)
# print(pm_author)

# 안건


def topic_extractor(text):
    pm_topi = []
    pm_topic = []
    pm_topict = []
    pm_topicc = []
    s_start = False
    s_end = False
    break_early = False
    # s_sent = []
    for i in range(len(text)):
        sent = text[i].strip()
        if sent == '상정된 안건' or sent == '審査된案件' or sent == '심사된 안건':
            s_start = i
        if sent.endswith('개의)'):
            s_end = i - 5
            break_early = True
            if break_early:
                break
    while s_start <= s_end:
        s_start += 1
        topic = text[s_start].split('\t')
        topic = hanja.translate(topic[0], "substitution")
        topic.strip()
        pm_top = topic.split('\n')
        pm_topi += pm_top
    # pprint(pm_topi)
    # pm_topi = (sorted(pm_topi))
    # pprint(len(pm_topi))

    if pm_topi[-1].endswith(")"):
        for s in range(len(pm_topi)):
            if not (pm_topi[s].startswith("가") or pm_topi[s].startswith("나") or pm_topi[s].startswith("다") or pm_topi[s].startswith("라") or pm_topi[s].startswith("마")):
                pm_topic1 = pm_topi[s] + " / "
                pm_topicc += pm_topic1.split('\n')
        pm_topicc[-1] = pm_topicc[-1].replace(" / ", "")
        # pprint(pm_topicc)
    elif len(pm_topi) == 1:
        pm_topicc += pm_topi
    elif pm_topi[0].startswith("1") and pm_topi[1].startswith("2"):
        for s in range(len(pm_topi)):
            pm_topic1 = pm_topi[s] + " / "
            pm_topicc += pm_topic1.split('\n')
        pm_topicc[-1] = pm_topicc[-1].replace(" / ", "")
    else:
        for n in range(len(pm_topi)):
            for m in range(len(pm_topi)):
                if pm_topi[n].startswith("{}".format(m)) and pm_topi[n+1].startswith("가"):
                    pm_topic1 = pm_topi[n] + " > "
                    pm_topicc += pm_topic1.split('\n')
                elif pm_topi[n].startswith("{}".format(m)) and not pm_topi[n+1].startswith("가"):
                    pm_topicc += pm_topi[n] + " / "
            if pm_topi[n].startswith("가") or pm_topi[n].startswith("나") or pm_topi[n].startswith("다") or pm_topi[n].startswith("라"):
                pm_topicc += pm_topi[n].split('\n')
    # pprint(pm_topicc)
    x = range(len(pm_topi))
    y = range(1, len(pm_topi))

    for a, b in zip(x, y):
        if pm_topicc[a].startswith("가") and pm_topicc[b].startswith("나"):
            pm_topicc[a] = pm_topicc[a] + ", "
        if pm_topicc[a].startswith("나") and pm_topicc[b].startswith("다"):
            pm_topicc[a] = pm_topicc[a] + ", "
        if pm_topicc[a].startswith("가") and not pm_topicc[b].startswith("나"):
            pm_topicc[a] = pm_topicc[a] + " / "
        if pm_topicc[a].startswith("나") and not pm_topicc[b].startswith("다"):
            pm_topicc[a] = pm_topicc[a] + " / "
        if pm_topicc[a].startswith("다") and not pm_topicc[b].startswith("라"):
            pm_topicc[a] = pm_topicc[a] + " / "
    for f in range(len(pm_topicc)):
        pm_topict += pm_topicc[f].split('\n')
        pm_topic = ''.join(pm_topict)

    return pm_topic


pm_topic = topic_extractor(text)

# pprint(pm_topic)

# 안건
# def topic_extractor(text):
#   pm_topic =[]
#   s_start = False
#   s_end = False
#   break_early = False
#   # s_sent = []
#   for i in range(len(text)):
#     sent = text[i].strip()
#     if sent == '상정된 안건' or sent == '審査된案件' or sent == '심사된 안건':
#       s_start = i
#     if sent.endswith('개의)'):
#       s_end = i - 5
#       break_early = True
#       if break_early:
#         break
#   while s_start <= s_end:
#     s_start += 1
#     topic = text[s_start].split('\t')
#     topic = hanja.translate(topic[0],"substitution")
#     topic.strip()
#     pm_top = topic.split('\n')
#     pm_topic += pm_top
#     # pprint(pm_topic)
#   return pm_topic
# pm_topic = topic_extractor(text)
# pprint(pm_topic)

# 메타데이터


def meta_extractor(text, pm_date, pm_topic, pm_author, fname):

    meta = {}
    # 카테고리
    pm_category = ''
    for i in range(3, 4):
        pm_category += text[i]
        pm_cate = hanja.translate(pm_category, 'substitution')

    pm_category = "회의록 > 국회소위원회 > " + pm_cate
    meta['카테고리'] = pm_category

    pm_code = ''
    for i in range(1, 6):
        pm_code += text[i]
        pm_code = hanja.translate(pm_code, 'substitution')
    pm_code = pm_code.replace(" ", "")
    meta['회의록코드'] = pm_code
    # print(pm_code_)

    # 국회명
    pm_name_ = ""
    for i in range(1, 3):
        pm_name_ += text[i]
        pm_name = hanja.translate(pm_name_, 'substitution')

    meta['국회명'] = pm_name
    # print(pm_name)

    # 회의록 제목
    pm_title = ''
    for i in range(3, 5):
        pm_title += text[i]
        pm_title = hanja.translate(pm_title, 'substitution')
    pm_title = pm_title.replace(" ", "")
    meta['회의록제목'] = pm_title
    # print(pm_title_)

    # 작성자
    meta['작성'] = pm_author

    # 일시
    meta['일시'] = pm_date

    # 토픽
    meta['토픽'] = pm_topic

    # 파일명
    f_title = ''
    f_title = fname.split('/')[-1].split('.txt')[0]
    f_title1 = unicodedata.normalize('NFD', f_title)
    file_title = unicodedata.normalize('NFC', f_title1)
    meta['파일명'] = file_title

    return meta


meta = meta_extractor(text, pm_date, pm_topic, pm_author, fname)
# pprint(meta)

# 본격적 대화(한글화버전)


def dialog_extractor(text):
    dialog = []
    doc = []
    # 대사 추출 프로그램
    # text는 전체를 아우르는 리스이다.
    # 이렇게 하면 doc는 1줄씩 나눈거
    for page in text:
        sents = page.split('\n')
        doc.append(sents)
    s_start = False
    s_end = False
    break_early = False
    # for i in range(len(doc)):
    #     page = doc[i]
    for sid in range(len(text)):
        sent = text[sid].strip()
        if sent.startswith('◯'):
            s_start = sid
            break_early = True
            break
        if break_early:
            break
    for sid in range(len(text)):
        sent = text[sid].strip()
        if sent.endswith('산회)') or sent.endswith('중지)'):
            s_end = sid
    for sid in range(len(text)):
        sent = text[sid].strip()
    break_early = False
    doc = []
    for sid in range(len(text)):
        if sid >= s_start and sid <= s_end - 1:
            sent = text[sid].strip()
            # ////////
            sent = hanja.translate(sent, 'substitution').replace("金", "김").replace("李", "이").replace("梁", "양").replace("羅", "나").replace("利", "이").replace(
                "勞", "노").replace("樂", "락").replace("盧", "노").replace("樂", "락").replace("龍", "용").replace("沈", "심").replace("呂", "려").replace("寧", "영").replace("宅", "택")
            # print(sent)
            if sent.endswith(")"):
                continue
            if sent.startswith('◯'):
                speaker = ' '.join(text[sid].split(' ')[0:3])
                tokens = ' '.join(text[sid].split(' ')[3:])
                sent1 = sent.replace('◯', '◯ ')
                doc.append(sent1)
            else:
                doc.append(sent)
    doc_p = ''.join(doc)
    # pprint(doc_p)
    doc_ps = doc_p.split('◯')
    # print(doc_ps)
    rev_doc = []
    for s in doc_ps:
        # if s.startswith('('):
        #     rev_doc.append(s)
        if s == '':
            pass
        elif s.startswith(" "):
            s = '◯'+s
            rev_doc.append(s)
        else:
            rev_doc.append(s)
    # doc_text = '\n'.join(rev_doc)
    # rev_doc = hanja.translate(rev_doc,'substitution')
    # pprint(rev_doc)
    dialog += rev_doc

    return dialog


dialog = dialog_extractor(text)
# pprint(dialog)

# 본격적 대화(원본)


def dialog_extractor_or(text_or):
    dialog_or = []
    doc = []
    # 대사 추출 프로그램
    # text는 전체를 아우르는 리스이다.
    # 이렇게 하면 doc는 1줄씩 나눈거
    for page in text_or:
        sents = page.split('\n')
        doc.append(sents)
    s_start = False
    s_end = False
    break_early = False
    # for i in range(len(doc)):
    #     page = doc[i]
    for sid in range(len(text_or)):
        sent = text_or[sid].strip()
        if sent.startswith('◯'):
            s_start = sid
            break_early = True
            break
        if break_early:
            break
    for sid in range(len(text_or)):
        sent = text_or[sid].strip()
        if sent.endswith('산회)') or sent.endswith('중지)'):
            s_end = sid

    for sid in range(len(text_or)):
        sent = text_or[sid].strip()
    break_early = False
    doc = []
    for sid in range(len(text_or)):
        if sid >= s_start and sid <= s_end - 1:
            sent = text_or[sid].strip()
            # ////////
            # print(sent)
            if sent.endswith(")"):
                continue
            if sent.startswith('◯'):
                speaker = ' '.join(text_or[sid].split(' ')[0:3])
                tokens = ' '.join(text_or[sid].split(' ')[3:])
                sent1 = sent.replace('◯', '◯ ')
                doc.append(sent1)
            else:
                doc.append(sent)
    # pprint(doc)
    doc_p = ''.join(doc)
    # pprint(doc_p)
    doc_ps = doc_p.split('◯')
    # print(doc_ps)
    rev_doc = []
    for s in doc_ps:
        # if s.startswith('('):
        #     rev_doc.append(s)
        if s == '':
            pass
        elif s.startswith(" "):
            s = '◯'+s
            rev_doc.append(s)
        else:
            rev_doc.append(s)
    # doc_text = '\n'.join(rev_doc)
    # rev_doc = hanja.translate(rev_doc,'substitution')
    # pprint(rev_doc)
    dialog_or += rev_doc

    return dialog_or


dialog_or = dialog_extractor_or(text_or)
# pprint(dialog_or)

# 대화에 참여자 이름, 직위


def speaker_extractor(dialog):
    global persons
    persons = []

    occups = []
    speaker_ex = []
    for i in range(len(dialog)):
        dialog_s = dialog[i].split(' ')
        first_t = dialog_s[1]
        second_t = dialog_s[2]
        # print(dialog_s)
        # if first_t.endswith("관") or first_t.endswith("장") or first_t.endswith("위원") or first_t.endswith("참고인") and len(first_t) >= 3:
        if second_t != "의원" and second_t != "위원" and second_t != "委員":
            occup = first_t.replace("◯ ", "")
        else:
            person = first_t.replace("◯ ", "")
        if second_t == "의원" or second_t == "위원" or second_t == "委員":
            occup = second_t
        else:
            person = second_t

        persons.append(person)
        occups.append(occup)
    # print(persons[0] +" " + occups[0])
    po = []
    for j in range(len(persons)):
        sp = persons[j] + " " + occups[j]
        po.append(sp)

    n_po = []
    for v in po:
        if v not in n_po:
            n_po.append(v)
    for w in range(len(n_po)):
        n_pos = n_po[w].split(' ')
        speaker_ex.append(n_pos)
    return speaker_ex


speaker_ex = speaker_extractor(dialog)
# pprint(speaker_ex)

# 발언자, 발언(한글수정)


def utterance_extractor(dialog):
    utterance_id = []
    utterance_form = []

    for i in range(len(dialog)):
        dialog_s = dialog[i].split(' ')
        # first_s = dialog_s[1:3]
        second_s = dialog_s[4:]
        # spk_id = ' '.join(first_s)
        utter = ' '.join(second_s)
        # utterance_id.append(spk_id)
        utterance_form.append(utter)

    return persons, utterance_form


utterance_ex = utterance_extractor(dialog)
# pprint(utterance_ex)

# 발언자, 발언(원본)


def utterance_extractor_or(dialog_or):
    utterance_id = []
    utterance_form = []

    for i in range(len(dialog_or)):
        dialog_s = dialog_or[i].split(' ')
        first_s = dialog_s[1:3]
        second_s = dialog_s[4:]
        spk_id = ' '.join(first_s)
        utter = ' '.join(second_s)
        utterance_id.append(spk_id)
        utterance_form.append(utter)
    return utterance_id, utterance_form


utterance_ex_or = utterance_extractor_or(dialog_or)
# pprint(utterance_ex_or)

# utterance info(원본, 한글버전)


def dialog_formatting(utterance_ex, utterance_ex_or):
    dialog_json = []
    utterance_id = utterance_ex[0]
    utterance_form = utterance_ex[1]
    utterance_form_or = utterance_ex_or[1]
    # pprint(utterance_form_or)
    for i in range(len(utterance_ex[0])):
        d = {}
        d['speaker'] = utterance_id[i]
        d['utterance'] = utterance_form[i]
        d['utterance_or'] = utterance_form_or[i]

        dialog_json.append(d)

    # result.append(d)
    return dialog_json


dialog_json = dialog_formatting(utterance_ex, utterance_ex_or)
# pprint(dialog_json)

# speaker info


def speaker_list_extractor(speaker_ex):
    global p_name
    p_name = []
    p_name1 = []
    speaker_list = []
    speaker = []

    for i in range(len(speaker_ex)):
        name = speaker_ex[i][0]
        position = speaker_ex[i][1]
        if position != "소위원장대리":
            d = {}
            d['id'] = name
            d['age'] = "NA"
            d['occupation'] = position
            d['sex'] = "NA"
            d['birthplace'] = "NA"
            d['principal_residence'] = "NA"
            d['current_residence'] = "NA"
            speaker_list.append(d)
            p_name.append(d['id'])

    # print(p_name)
    return speaker_list


speaker_list = speaker_list_extractor(speaker_ex)
# pprint(speaker_list)


# 산회 이하 문장(형태가 복잡해서 사용 불가)
def speaker_extractor2(text, speaker_list, speaker_ex):

    s_start = False
    ss_start = False
    break_early = False
    s_sentence = []
    ss_sentence = []
    sss_sentence = []
    c_sentence = []
    d_sentence = []
    speaker_list2 = []
    speaker_list2__ = []
    e_sentence = []
    f_sentence = []
    B_member = []
    part2 = False
    part3 = False
    part4 = False
    c_end = False
    d_end = False
    e_end = False
    role = ""
    b = 0

    # 산회) 이하 제~일) 이상 문장 뽑기
    for i in range(len(text)):
        if text[i].endswith("산회)") or text[i].endswith('중지)'):
            s_start = i + 1
    #     break_early = True
    #     break
    # break_early = False
    for i in range(len(text)):
        if text[i].startswith("제") and (text[i].endswith('일)') or text[i].endswith('차')):
            if text[i - 1] == '':
                s_end = i - 2
                break_early = True
                break
            break_early = False
            if text[i - 1] != '':
                s_end = i
                break_early = True
                break
            break_early = False

    for sid in range(len(text)):
        if sid >= s_start and sid < s_end:
            sub_sentences = hanja.translate(text[sid], "substitution").replace("金", "김").replace("李", "이").replace("梁", "양").replace("羅", "나").replace(
                "利", "이").replace("勞", "노").replace("樂", "락").replace("盧", "노").replace("樂", "락").replace("龍", "용").replace("沈", "심").replace("宅", "택")
            s_sentence.append(sub_sentences)

    # 출석 위원
    for j in range(len(s_sentence)):
        if s_sentence[j].startswith("◯") or s_sentence[j].startswith("○"):
            m = j + 1
            A_member = s_sentence[m].split("  ")
            break_early = True
            break
    break_early = False
    # pprint(A_member)
    # p_name2 = []
    for t in range(len(A_member)):
        if A_member[t] not in p_name:
            name = A_member[t]
            d = {}
            d['id'] = name
            d['age'] = "NA"
            d['occupation'] = "위원"
            d['sex'] = "NA"
            d['birthplace'] = "NA"
            d['principal_residence'] = "NA"
            d['current_residence'] = "NA"
            speaker_list2.append(d)
    # pprint(speaker_list2)
    for u in range(len(s_sentence)):
        if s_sentence[u] == "" and s_sentence[u+1] == "":
            first_line_end = u
            break_early = True
            break
    break_early = False

    # 위원 아닌 출석 의원(X인)
    for e in range(len(s_sentence)):
        if e > m and e < first_line_end:
            ss_sentence += s_sentence[e].split("\n")
    for a in range(len(ss_sentence)):
        # 수정했는데 맞겠지?
        if (ss_sentence[a].startswith("◯") or ss_sentence[a].startswith("○")) and ss_sentence[a].endswith("인)"):
            if ss_sentence[a].startswith("◯위원") or ss_sentence[a].startswith("○위원"):
                b = a + 1
                B_member = ss_sentence[b].split('  ')
                occup = "의원"
                break
            else:
                b = a + 1
                B_member = ss_sentence[b].split('  ')
                occup = "위원"
                break
    for y in range(len(B_member)):
        if B_member[y] not in p_name:
            name = B_member[y]
            d = {}
            d['id'] = name
            d['age'] = "NA"
            d['occupation'] = occup
            d['sex'] = "NA"
            d['birthplace'] = "NA"
            d['principal_residence'] = "NA"
            d['current_residence'] = "NA"
            speaker_list2.append(d)

    # 위원 아닌 출석 의원(X인)2
    if ss_sentence[b+1].endswith("인)") == True:
        for e in range(len(s_sentence)):
            if e > m and e < first_line_end:
                ss_sentence += s_sentence[e].split("\n")
        for a in range(len(ss_sentence)):
            # 수정했는데 맞겠지?
            if (ss_sentence[a].startswith("◯") or ss_sentence[a].startswith("○")) and ss_sentence[a].endswith("인)"):
                if ss_sentence[a].startswith("◯위원") or ss_sentence[a].startswith("○위원"):
                    b = a + 1
                    B_member = ss_sentence[b].split('  ')
                    occup = "의원"
                else:
                    b = a + 1
                    B_member = ss_sentence[b].split('  ')
                    occup = "위원"

        for y in range(len(B_member)):
            if B_member[y] not in p_name:
                name = B_member[y]
                d = {}
                d['id'] = name
                d['age'] = "NA"
                d['occupation'] = occup
                d['sex'] = "NA"
                d['birthplace'] = "NA"
                d['principal_residence'] = "NA"
                d['current_residence'] = "NA"
                speaker_list2.append(d)
    # print(speaker_list2)

    # 출석 전문위원
    for a in range(len(ss_sentence)):
        if not ss_sentence[a].endswith("인)") and (ss_sentence[a].startswith("◯") or ss_sentence[a].startswith("○")):
            s_start = a+1
    for z in range(len(ss_sentence)):
        if z >= s_start:
            sss = ss_sentence[z].split("\n")
            sss_sentence += sss
    count = int(len(sss_sentence) / 2)
    id_s = range(count, len(sss_sentence))
    ocu_s = range(0, count)
    for n, m in zip(id_s, ocu_s):
        if sss_sentence[n] not in p_name:
            d = {}
            d['id'] = sss_sentence[n]
            d['age'] = "NA"
            d['occupation'] = sss_sentence[m]
            d['sex'] = "NA"
            d['birthplace'] = "NA"
            d['principal_residence'] = "NA"
            d['current_residence'] = "NA"
            speaker_list2.append(d)
    # pprint(speaker_list2)
    # # 위원 의원 아래
    for p in range(len(s_sentence)):
        if s_sentence[p].startswith("◯") and s_sentence[p].endswith("참석자"):
            part = p + 1
            c = p + 2
            c_part = s_sentence[part]
            break
    for l in range(len(s_sentence)):
        if l >= part:
            if s_sentence[l] == "" and s_sentence[l+1] == "":
                c_end = l
                break
            else:
                c_end = l + 1
    for m in range(len(s_sentence)):
        if m >= part and m < c_end:
            ssss = s_sentence[m].split('\n')
            c_sentence += ssss
    # pprint(c_sentence)
    count = int((len(c_sentence) - 1) / 2) + 1
    id_c = range(count, len(c_sentence))
    ocu_c = range(1, count)
    for n, m in zip(id_c, ocu_c):
        if c_sentence[n] not in p_name:
            d = {}
            d['id'] = c_sentence[n]
            d['age'] = "NA"
            d['occupation'] = c_part + c_sentence[m]
            d['sex'] = "NA"
            d['birthplace'] = "NA"
            d['principal_residence'] = "NA"
            d['current_residence'] = "NA"
            speaker_list2.append(d)
    # print(s_sentence[c_end-1])

    # 그다음꺼 있으면
    if c_end != False:
        for h in range(len(s_sentence)):
            if h > c_end:
                if s_sentence[c_end] == "" and s_sentence[c_end+1] == "" and not s_sentence[c_end+2].startswith("◯"):
                    part2 = c_end + 2
                    d_part = s_sentence[part2]
                    break
        # print(part2)
        if part2 != False:
            for r in range(len(s_sentence)):
                if r >= part2:
                    if s_sentence[r] == "" and s_sentence[r+1] == "":
                        d_end = r
                        break
                    else:
                        d_end = r + 1
            # print(d_end)
        if part2 != False:
            for m in range(len(s_sentence)):
                if m >= part2 and m < d_end:
                    sssss = s_sentence[m].split('\n')
                    d_sentence += sssss
            # pprint(d_sentence)
            count = int((len(d_sentence) - 1) / 2) + 1
            id_d = range(count, len(d_sentence))
            ocu_d = range(1, count)
            for n, m in zip(id_d, ocu_d):
                if d_sentence[n] not in p_name:
                    d = {}
                    d['id'] = d_sentence[n]
                    d['age'] = "NA"
                    d['occupation'] = d_part + d_sentence[m]
                    d['sex'] = "NA"
                    d['birthplace'] = "NA"
                    d['principal_residence'] = "NA"
                    d['current_residence'] = "NA"
                    speaker_list2.append(d)
        # pprint(speaker_list2)

    # 그다음꺼 있으면2
    if d_end != False:
        for h in range(len(s_sentence)):
            if h > d_end:
                if s_sentence[d_end] == "" and s_sentence[d_end+1] == "" and not s_sentence[d_end+2].startswith("◯"):
                    part3 = d_end + 2
                    e_part = s_sentence[part3]
                    break
        # print(part2)
        if part3 != False:
            for r in range(len(s_sentence)):
                if r >= part3:
                    if s_sentence[r] == "" and s_sentence[r+1] == "":
                        e_end = r
                        break
                    else:
                        e_end = r + 1
        if part3 != False:
            for m in range(len(s_sentence)):
                if m >= part3 and m < e_end:
                    ssssss = s_sentence[m].split('\n')
                    e_sentence += ssssss
            # pprint(d_sentence)
            count = int((len(e_sentence) - 1) / 2) + 1
            id_e = range(count, len(e_sentence))
            ocu_e = range(1, count)
            for n, m in zip(id_e, ocu_e):
                if e_sentence[n] not in p_name:
                    d = {}
                    d['id'] = e_sentence[n]
                    d['age'] = "NA"
                    d['occupation'] = e_part + e_sentence[m]
                    d['sex'] = "NA"
                    d['birthplace'] = "NA"
                    d['principal_residence'] = "NA"
                    d['current_residence'] = "NA"
                    speaker_list2.append(d)
    # # 그다음꺼 있으면3
    if e_end != False:
        for h in range(len(s_sentence)):
            if h > e_end:
                if s_sentence[e_end] == "" and s_sentence[e_end+1] == "" and not s_sentence[e_end+2].startswith("◯"):
                    part4 = e_end + 2
                    f_part = s_sentence[part4]
                    break
        # print(part2)
        if part4 != False:
            for r in range(len(s_sentence)):
                if r >= part4:
                    if s_sentence[r] == "" and s_sentence[r+1] == "":
                        f_end = r
                        break
                    else:
                        f_end = r + 1
        if part4 != False:
            for m in range(len(s_sentence)):
                if m >= part4 and m < f_end:
                    sssssss = s_sentence[m].split('\n')
                    f_sentence += sssssss
            # pprint(d_sentence)
            count = int((len(f_sentence) - 1) / 2) + 1
            id_f = range(count, len(f_sentence))
            ocu_f = range(1, count)
            for n, m in zip(id_f, ocu_f):
                if f_sentence[n] not in p_name:
                    d = {}
                    d['id'] = f_sentence[n]
                    d['age'] = "NA"
                    d['occupation'] = f_part + f_sentence[m]
                    d['sex'] = "NA"
                    d['birthplace'] = "NA"
                    d['principal_residence'] = "NA"
                    d['current_residence'] = "NA"
                    speaker_list2.append(d)

    # 진술인 참고인
    for f in range(len(s_sentence)):
        if s_sentence[f].startswith("◯") and (s_sentence[f].endswith("진술인") or s_sentence[f].endswith("참고인")):
            role = s_sentence[f].split(" ")[1]
            ss_start = f + 1
    if ss_start != False:
        # print(s_start)
        for j in range(len(s_sentence)):
            if j >= ss_start:
                ee = s_sentence[j].split("(")
                eee = ee[0].split('\n')
                e_sentence += eee
        for n in range(len(e_sentence)):
            if e_sentence[n] not in p_name:
                d = {}
                d['id'] = e_sentence[n]
                d['age'] = "NA"
                d['occupation'] = role
                d['sex'] = "NA"
                d['birthplace'] = "NA"
                d['principal_residence'] = "NA"
                d['current_residence'] = "NA"
                speaker_list2.append(d)

    # print(p_name)
    for last in range(len(speaker_list2)):
        if speaker_list2[last]['id'] not in p_name:
            d = {}
            d['id'] = speaker_list2[last]['id']
            d['age'] = "NA"
            d['occupation'] = speaker_list2[last]['occupation']
            d['sex'] = "NA"
            d['birthplace'] = "NA"
            d['principal_residence'] = "NA"
            d['current_residence'] = "NA"
            speaker_list2__.append(d)
            # print(speaker_list2__[last]['id'])

    # print(speaker_list2[0]['id'])
    return speaker_list2__


speaker_list2__ = speaker_extractor2(text, speaker_list, speaker_ex)
# pprint(speaker_list2__)

# json 형태로 변환하기 위한 틀


def convert_to_korea(meta, speaker_list, speaker_list2__, dialog_json, id):
    # k = 0
    id = "SBRW 2100000001"
    # id_code = korea_formatted_data['id']
    # id = id_code.split(" ")
    # id0 = id[0]
    # id1 = int(id[1]) + k
    # id = id0 + str(id1)
    # korea_formatted_data['id'] = id
    # k += 1

    metadata = {}
    metadata['title'] = "국립국어원 국회 회의록 원시 말뭉치 " + id
    metadata['creator'] = "국립국어원"
    metadata['distributor'] = "국립국어원"
    metadata['year'] = "2021"
    metadata['category'] = meta['카테고리']
    metadata['annotation_level'] = ['원시']
    metadata['sampling'] = "본문 전체"

    doc = {}
    doc['id'] = id+".1"
    doc_metadata = {}
    doc_metadata['title'] = meta['회의록제목']
    doc_metadata['author'] = meta['작성']
    # doc_metadata['author_id'] = ""
    doc_metadata['publisher'] = meta['작성']
    doc_metadata['date'] = meta['일시']
    doc_metadata['topic'] = meta['토픽']
    # pprint(doc_metadata['topic'])
    # doc_metadata['original_topic'] = ""
    # doc_metadata['crawl_date'] = ""

    doc_metadata['speaker'] = speaker_list + speaker_list2__
    # pprint(doc_metadata['speaker'])
    doc_metadata['setting'] = {}
    doc_metadata['setting']['relation'] = "NA"

    doc_metadata['file_id'] = meta['파일명']
    # '회의록 원문 자료 파일명:'

    doc['metadata'] = doc_metadata

    # doc['paragraph'] = []
    # paragraph = {}
    # paragraph['id'] = ""
    # paragraph['form'] = ""
    # paragraph['original_form'] = ""
    # doc['paragraph'].append(paragraph)

    utterance = []

    n = 0
    for i in dialog_json:
        utter = {}
        utter['id'] = id+".1.1." + str(n+1)
        utter['form'] = i['utterance']
        utter['original_form'] = i['utterance_or']
        utter['speaker_id'] = i['speaker']
        utter['note'] = ""
        utterance.append(utter)
        n += 1
        # pprint(utter['id'])
    doc['utterance'] = utterance

    d = {}
    d['id'] = id
    d['metadata'] = metadata
    d['document'] = doc

    return d


korea_formatted_data = convert_to_korea(
    meta, speaker_list, speaker_list2__, dialog_json, id)
# pprint(korea_formatted_data)
# pprint(korea_formatted_data['document']['utterance'][0])


# argparse 이용 터미널로 불러오기
parser = argparse.ArgumentParser(description='list to json')
parser.add_argument('--input', metavar='', type=str,
                    required=True, help='Input Folder')
parser.add_argument('--output', metavar='', type=str,
                    required=True, help='Output Folder')
args = parser.parse_args()
# json 형태로 변환


def txt_reader(input, output, id):
    k = 0
    files = sorted(glob(input + "*.txt"))
    for fname in files:
        with open(fname, 'r', encoding='utf-8-sig') as file:
            txt = file.readlines()
            pass
            text = clean_up(txt)
            text_or = clean_up_or(txt)
            pm_date = date_extractor(text)
            pm_author = author(text)
            pm_topic = topic_extractor(text)
            meta = meta_extractor(text, pm_date, pm_topic, pm_author, fname)
            dialog = dialog_extractor(text)
            dialog_or = dialog_extractor_or(text_or)
            speaker_ex = speaker_extractor(dialog)
            utterance_ex = utterance_extractor(dialog)
            utterance_ex_or = utterance_extractor_or(dialog_or)
            dialog_json = dialog_formatting(utterance_ex, utterance_ex_or)
            speaker_list = speaker_list_extractor(speaker_ex)
            speaker_list2__ = speaker_extractor2(
                text, speaker_list, speaker_ex)
            korea_formatted_data = convert_to_korea(
                meta, speaker_list, speaker_list2__, dialog_json, id)
            id = "SBRW 2100000001"
            id_code = id.split(" ")
            id0 = id_code[0]
            id1 = int(id_code[1]) + k
            id_code = id0 + str(id1)
            korea_formatted_data['id'] = id_code
            korea_formatted_data['metadata']['title'] = "국립국어원 국회 회의록 원시 말뭉치 " + id_code
            korea_formatted_data['document']['id'] = id_code + ".1"

            n = 0
            for i in dialog_json:
                korea_formatted_data['document']['utterance'][n]['id'] = id_code + \
                    ".1.1." + str(n+1)
                n += 1
            k += 1
        fname_write = fname.split('/')[-1].split('.txt')[0]

        with open(output+fname_write+'.json', 'w') as f:
            json.dump(korea_formatted_data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    txt_reader(args.input, args.output, id)
