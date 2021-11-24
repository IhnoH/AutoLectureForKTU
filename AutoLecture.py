import sys
from PyQt5.QtWidgets import *
from selenium import webdriver
from datetime import datetime
import time
import threading
import os.path
import sys
import chromedriver_autoinstaller
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

login_id = ''
login_pw = ''

t = []
s = 0
_t = 0
lsn_name = []
n = ''

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_login = False
        self.is_listening = False
        self.x = AutoLecture()

        self.lb_id = QLabel('ID', self)
        self.lb_id.move(20, 23)
        self.lb_pw = QLabel('PW', self)
        self.lb_pw.move(20, 48)

        self.input_id = QLineEdit(self)
        self.input_id.resize(120, 20)
        self.input_id.move(50, 26)

        self.input_pw = QLineEdit(self)
        self.input_pw.setEchoMode(QLineEdit.Password)
        self.input_pw.resize(120, 20)
        self.input_pw.move(50, 51)

        self.bt_login = QPushButton('로그인', self)
        self.bt_login.move(180, 28)
        self.bt_login.resize(80, 20)
        self.bt_login.clicked.connect(self.get_login_info)

        self.whole = QPushButton('모두 학습', self)
        self.whole.move(380, 28)
        self.whole.resize(80, 20)
        self.whole.clicked.connect(self.whole_lessen)

        self.quit = QPushButton('학습 중단', self)
        self.quit.move(380, 51)
        self.quit.resize(80, 20)
        self.quit.clicked.connect(self.quit_listen)

        self.devel_info = QLabel('Made by Ihno Ver_2.1', self)
        self.devel_info.resize(200, 15)
        self.devel_info.move(500, 25)

        self.log = QTextEdit(self)
        self.log.resize(350, 500)
        self.log.move(500, 45)

        self.progress = QLineEdit(self)
        self.progress.resize(120, 20)
        self.progress.setGeometry(500, 550, 350, 20)

        self.tip = QLabel('Info를 읽어주세요', self)
        self.tip.resize(200, 15)
        self.tip.move(20, 550)

        self.menu_bar = self.menuBar()
        self.menu_bar.setNativeMenuBar(False)
        self.readme = QAction('ReadMe(info)', self)
        self.readme.triggered.connect(self.readme_open)

        self.release = QAction('Release', self)
        self.release.triggered.connect(self.release_open)

        self.file_menu = self.menu_bar.addMenu('&Info')
        self.file_menu.addAction(self.readme)
        self.file_menu.addAction(self.release)

        self.dialog = QDialog()

        self.setWindowTitle('AutoLecture')
        self.setGeometry(300, 300, 900, 580)
        self.show()

    def readme_open(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle('README')
        self.lb2 = QLabel('- 첫 로그인 이후에 login_info.bin 로그인 정보 파일이 생성됩니다.\n', self)
        self.lb3 = QLabel('  이후에는 로그인 버튼만 누르면 로그인이 가능합니다.\n', self)
        self.lb4 = QLabel('- 아우누리 접속 종료 후에 사용해주세요.\n', self)
        self.lb5 = QLabel('- 모든 학습 종료 후 자동으로 로그아웃 됩니다.\n', self)
        self.lb6 = QLabel('- 하단 진행도 텍스트를 만지지 말아주세요 강제종료됩니다.\n', self)
        self.lb7 = QLabel('- 가급적 학습 중단을 누르고 종료해주세요. 학습 시간이 적용 되지 않을 수 있습니다.\n', self)

        self.boxlayout = QVBoxLayout()
        self.boxlayout.addWidget(self.lb2)
        self.boxlayout.addWidget(self.lb3)
        self.boxlayout.addWidget(self.lb4)
        self.boxlayout.addWidget(self.lb5)
        self.boxlayout.addWidget(self.lb6)
        self.boxlayout.addWidget(self.lb7)

        self.dialog.setLayout(self.boxlayout)
        self.dialog.show()

    def release_open(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle('Release')
        self.lb2 = QLabel('Ver_2.1', self)
        self.lb3 = QLabel('- try-except 클릭 후 딜레이 추가로 accept할 수 있게 수정', self)
        self.lb4 = QLabel('- QApplication, MyApp 자체를 쓰레드로 실행함으로 팅김현상 완화\n', self)

        self.boxlayout = QVBoxLayout()
        self.boxlayout.addWidget(self.lb2)
        self.boxlayout.addWidget(self.lb3)
        self.boxlayout.addWidget(self.lb4)

        self.dialog.setLayout(self.boxlayout)
        self.dialog.show()

    def closeEvent(self, event):
        self.deleteLater()
        super().closeEvent(event)

    def get_login_info(self):
        if self.is_login:
            print('이미 로그인 되어있음')
            self.log.append('이미 로그인 되어있습니다.')
            return
        global login_pw, login_id
        login_id = self.input_id.text()
        self.input_id.setText('')
        login_pw = self.input_pw.text()
        self.input_pw.setText('')
        self.is_login = self.x.login(login_id, login_pw)

    def whole_lessen(self):
        if self.is_listening:
            self.log.append('이미 학습중입니다.')
            return
        if self.is_login:
            self.log.append('모든 강의 학습 시작')
            self.is_listening = True
            threading.Thread(target=self.x.whole).start()
        else: self.log.append('로그인하지 않았습니다')

    def quit_listen(self):
        if self.is_listening:
            self.x.quit()
            self.log.append('학습이 중단되었습니다.')
        else: self.log.append('학습하지 않고 있습니다.')

class AutoLecture:
    def __init__(self):
        chromedriver_autoinstaller.install(True)
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")
        option.add_argument("--disable-gpu")
        # option.add_argument('--start-fullscreen') #f11 전체화면 옵션
        self.driver = webdriver.Chrome(os.getcwd() + f'\{chrome_ver}\chromedriver.exe', options=option)
        global ex

    def isKor(self, word):
        if len(word) <= 0: return False
        # UNICODE RANGE OF KOREAN: 0xAC00 ~ 0xD7A3
        for c in range(len(word)):
            if word[c] < u"\uac00" or word[c] > u"\ud7a3": return False
        return True

    def toSec(self, word):
        if len(word) <= 0: return 0
        tmp = ''
        t = 0
        for i in word:
            if i == '시':
                t = t + int(tmp) * (60 ** 2)
                tmp = ''
            elif i == '분':
                t = t + int(tmp) * (60)
                tmp = ''
            elif i == '초':
                t = t + int(tmp)
                tmp = ''
            else: tmp = tmp + i
        return t

    def login(self, id='', pw=''):
        if len(id) != 0 and len(pw) != 0: id, pw = login_id, login_pw
        elif os.path.isfile(os.getcwd()+"\login_info.bin"):
            with open(os.getcwd() + "\login_info.bin", "rb") as f:
                byte = f.read()
                while byte != b"":
                    id, pw = byte.decode(encoding='utf-8').split('\n')
                    byte = f.read()
            print('정보 입력되지 않음')

        self.driver.get('https://el.koreatech.ac.kr/ilos/main/member/login_form.acl')
        self.driver.find_element_by_id("usr_id").send_keys(id)
        self.driver.find_element_by_id("usr_pwd").send_keys(pw)
        time.sleep(0.5)

        try:
            self.driver.find_element_by_id('login_btn').click()
            time.sleep(0.5)
            self.driver.switch_to.alert.accept()
            ex.log.append('로그인 실패: 아이디와 비밀번호를 다시 확인해 주세요')
            print('로그인 실패')
            return False
        except: pass
        with open(os.getcwd() + "\login_info.bin", "wb") as f: f.write(bytes('{}\n{}'.format(id, pw), encoding="utf-8"))
        ex.log.append('로그인 성공')
        print('로그인 성공 후 파일저장')
        print('--------')
        return True

    def whole(self):
        lec_name = self.driver.find_elements_by_class_name('sub_open')
        lec_name = [i.text for i in lec_name if '인권' not in i.text and '안전' not in i.text and '학습디딤돌' not in i.text and '장애' not in i.text]

        for i in range(2, 2 + len(lec_name)):  # 과목별 학습
            # 과목 선택
            ex.log.append(lec_name[i-2])
            lecture = '//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[%s]/em'%str(i)
            print(self.driver.find_element_by_xpath(lecture).text)

            self.driver.find_element_by_xpath(lecture).click()
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath(
                '//*[@id="menu_lecture_weeks"]').click()  # 온라인강의
            self.driver.implicitly_wait(5)

            info = self.driver.find_elements_by_class_name('wb-inner-wrap')
            week = [i.text.split('\n')[0][:-1] for i in info]

            for w in range(len(week)):  # 주차별 학습
                # 페이지 이동으로 인한 재추출
                info = self.driver.find_elements_by_class_name('wb-inner-wrap')
                week = [i.text.split('\n')[0][:-1] for i in info]
                progress = [i.text.split('\n')[1] for i in info]
                #print(week[w], ':', progress[w][0], progress[w][-1])

                #if progress[w][0] != progress[w][-1]:  # 모두 학습하지 않음
                info[w].click()
                self.driver.implicitly_wait(5)
                form = self.driver.find_elements_by_class_name('lecture-box')  # 강의 제목
                form = sum([j.text.split('\n') for j in form], [])
                if '아닙니다' in form: continue # 강의가 열려있지 않음
                date = [j for j in form if '학습인정기간' in j]
                date = [j.split('~ 2021.')[1].split(' 오')[0].split('.') for j in date]
                date = max([int(j[0])*30 + int(j[1]) for j in date])
                # 강의 수강 시간이 지났음
                if date < datetime.today().month * 30 + datetime.today().day: continue
                print('학습중')
                self.listen()

                #elif progress[w][0] == progress[w][-1]: print('이미 학습 완료')
            print()
            ex.log.append('')

            # 줌강의
            '''
            self.driver.find_element_by_xpath('//*[@id="menu_zoom"]').click()
            zoom = self.driver.find_elements_by_xpath('//*[@id="list_zone"]/table/tbody')
            for z in zoom: print('zoom 강의:', z.text)
            '''

            self.driver.find_element_by_xpath('//*[@id="logo_link"]').click()
            self.driver.implicitly_wait(5)

        self.driver.switch_to_default_content()
        self.driver.find_element_by_class_name('header_logout').click()
        ex.is_listening = False
        ex.is_login = False
        ex.log.append('학습 및 로그아웃 완료')
        print('학습 및 로그아웃 완료')

    def listen(self):  # 수업듣기
        lessen = self.driver.find_elements_by_class_name('site-mouseover-color')  # 학습하기 아이콘 이미지 클릭 용도
        lsn_name = [i.text for i in lessen]
        rate = [i.text for i in self.driver.find_elements_by_id('per_text')]  # 학습율 확인용도
        t = self.driver.find_elements_by_class_name('ibox2')
        t = sum([i.text.split('\n') for i in t], [])
        t = [i for i in t if ('분 /' in i or '초 /' in i or '시 /' in i)]
        t_origin = [self.toSec(i.split('/ ')[-1]) for i in t]  # 각 강의당 초
        t_had = [self.toSec(i.split(' /')[0]) for i in t]
        t = [t_origin[i] - t_had[i] for i in range(len(t))]
        for i in range(len(lessen)):
            action = ActionChains(self.driver)
            action.move_to_element(lessen[i]).perform()
            if rate[i] != '100%':
                print(lsn_name[i])
                print('----click----')
                try:
                    lessen[i].click()
                    time.sleep(0.5)
                    self.driver.switch_to.alert.accept()
                except: pass
                ex.log.append(lsn_name[i]+': 학습 중')
                print('go to sleep:', t[i])

                _t = t[i] + 15
                s = time.time()
                time.sleep(0.5)
                while ex.is_listening:
                    tmp = time.time() - s
                    p = round(tmp / _t * 100)
                    prog = '{2}: {0:.0f}s/{1}s - '.format(tmp, _t, lsn_name[i]) + str(p) + '%'

                    # print(prog, end='')
                    ex.progress.setText(prog)
                    time.sleep(0.5)
                    ex.progress.setText('')
                    # for a in range(len(prog) + 1): print('\r', end='')
                    if p >= 100: break
                else: return
                #print(time.time() - s)
                ex.log.append('학습 완료')
                try:
                    self.driver.find_element_by_xpath('//*[@id="close_"]').click()
                    print('-----close----')
                    time.sleep(0.5)
                    self.driver.switch_to.alert.accept()
                except: pass
            lessen = self.driver.find_elements_by_class_name('site-mouseover-color')  # 페이지 이동으로 인한 재추출



    def select(self, lec_n, driver):
        lecture = '//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[' + \
            str(lec_n) + ']/em'
        self.driver.find_element_by_xpath(lecture).click()
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_xpath(
            '//*[@id="menu_lecture_weeks"]').click()
        self.driver.implicitly_wait(5)

        # 페이지 이동으로 인한 재추출
        self.listen()
        self.driver.find_element_by_xpath('//*[@id="logo_link"]').click()
        self.driver.implicitly_wait(5)

    def quit(self):
        try:
            self.driver.find_element_by_xpath('//*[@id="close_"]').click()
            time.sleep(0.5)
            self.driver.switch_to.alert.accept()
        except: pass
        self.driver.find_element_by_xpath('//*[@id="logo_link"]').click()
        ex.is_listening = False

class Threading(threading.Thread):
    def __init__(self, parent=None):
        threading.Thread.__init__(self)
        self.parent = parent
        global ex

    def run(self):
        global ex
        app = QApplication(sys.argv)
        ex = MyApp()
        app.exec_()
        pass


if __name__ == '__main__':
    t = Threading()
    t.start()



