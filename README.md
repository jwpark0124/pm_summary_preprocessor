# txt_reader(text파일): 국회록 원시데이터 추출기(json파일)

### **visual studio code 기준으로 작성했습니다.
### ***install 및 import 문제가 있을시 프로그램을 종료 후 다시 실행해보시길 바랍니다.

## Installation

```
>>>pip install hanja
>>>pip install pyyaml
```

hanja를 import해도 인식하지 못한다면 txt_reader.py와 함께있는 파일들을 같은 폴더에 다운 그 폴더에서 pip install . 해줍니다.

yaml이 제 기능을 못한다면 팔레트를 열고
Python:Select Interpreter 클릭 후
제일 아래 version을 클릭해줍니다.

## Usage

파일 불러오기

```
fname = "/Users/jaewanpark/Documents/회의록/회의록 1차 2차 분류/1차/284여성(예산결산기금심사)소위01.txt"
```

경로를 본인의 텍스트 파일이 있는 바꿔주시고 저장해주세요.

```
>>>python txt_reader.py --input "/경로1/" --output "/경로2/"
```

경로1은 국회록 텍스트 파일이 있는 폴더의 경로이고
경로2는 json파일을 만들고 싶은 폴더의 경로입니다.

## 주의사항

```
1.hwp 파일을 txt 파일로 바꿔서 활용할 것
2.txt파일의 최하단의 참여자 목록의 형식이 일정하지 않아 몇가지 수정이 필요할 수 있음.
(요약대상회의록-1차)는 작성자에 의해 수정됨.
** 하위참조
```

hwp를 txt파일로 변경하기 위해 [Link](https://cloudconvert.com/hwp-to-txt/)를 이용함.

## \*\*참조사항

```
샘플폴더의 샘플파일을 열어 참조하십시오.
주의사항1
이름이 외자인 경우 성과 이름 사이의 공백은 1칸으로
주의사항2
'◯출석 위원(x인)' 같은 형태는 이름과 이름사이 공백을 2칸주고 한줄로 나열
주의사항3
'◯정부측 및 기타 참석자' 같은 혀앹는 첫번째 여성가족부같은 부서가 없을시 빈칸으로 남겨둠.
주의사항4
여성가족부 이후 직책 나열 후 순서에 맞게 이름 나열
(직책1 이름1),(직책2 이름2) 대응됨
```

### 오류사항이 있을시 수정 후 반영하겠습니다.
2021년08월06일

```
>>> 변경사항(1차 update) <<<
주의사항1
-> 이름이 외자인 경우 성과 이름 사이의 공백을 없앤다.
예) 이  완  -> 이완
```

2021년08월09일(월)
