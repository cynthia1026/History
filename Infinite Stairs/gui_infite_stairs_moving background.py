'''
무한의 계단 by 2517003 곽채원
=================================================
사용 방법:
- 1, 2, 3, 4: 게임 최초 실행 시 계단 테마 선택
- Enter: 게임 시작 및 재시작
- Left / Right: 왼쪽 또는 오른쪽 계단으로 이동
- Space: (치트키) 누르고 있는 동안 자동으로 계단을 오름
- Escape: 프로그램 종료
- Backspace : 현재 진행하는 판 중단 및 재시작 화면 돌아가기
'''

import gui_core as gui
import random

def generate_stair(last_x, last_y):
    direction = random.choice(['left', 'right'])
    new_x = last_x - 30 if direction == 'left' else last_x + 30
    new_y = last_y - 20
    
    rect_id = w.newImage(new_x, new_y, w.data.stair_theme, new_width=30, new_height=20)
    return {'rect': rect_id, 'dir': direction, 'x': new_x, 'y': new_y}

def raise_ui_and_character():
    # 새로 생성된 계단 밑으로 캐릭터나 UI가 깔리지 않도록 맨 위로 올리는 함수
    w.raiseObject(w.data.char_id)
    w.raiseObject(w.data.score_panel)
    w.raiseObject(w.data.score_text)
    w.raiseObject(w.data.info_text)

def initialize(timestamp):
    w.data.is_playing = False
    w.data.theme_selected = False 
    w.data.score = 0
    w.data.last_move_time = timestamp
    w.data.stairs = []
    
    w.data.theme_images = {'1': 'brick.png', '2': 'cement.png', '3': 'ice.png', '4': 'grass.png'}
    w.data.stair_theme = 'brick.png' 
    w.data.prev_keys = {k: False for k in ['return', 'left', 'right', 'backspace', 'escape', '1', '2', '3', '4', 'space']}
    
    # 1. 단일 통합 배경 이미지 (800x5400) 생성
    # 맨 아랫부분(지상 600px 영역)부터 시작하려면 y = -4800 (5400 - 600)이어야 함
    w.data.current_bg_y = -4800
    w.data.bg_id = w.newImage(0, w.data.current_bg_y, 'bg_full.png', new_width=800, new_height=5400)
    
    # 테마 고르는 첫 화면에서는 흰 배경만 보이도록 숨김
    w.hideObject(w.data.bg_id)
    
    # 2. 상단 점수 UI 패널
    w.data.score_panel = w.newRectangle(300, 20, 200, 40, fill_color="black")
    w.data.score_text = w.newText(400, 40, 200, text="점수: 0", fill_color="white", anchor='center')
    w.hideObject(w.data.score_panel)
    w.hideObject(w.data.score_text)
    
    # 3. 안내 문구 및 캐릭터
    w.data.info_text = w.newText(300, 300, 600, text="1~4번 키를 눌러 계단 테마를 선택하세요!\n(1: 벽돌, 2: 시멘트, 3: 얼음, 4: 풀)", fill_color="black", anchor='w')
    w.data.char_id = w.newImage(390, 360, 'character.png', new_width=35, new_height=60)
    w.hideObject(w.data.char_id)
    w.data.char_x = 400
    w.data.char_y = 360

def update(timestamp):
    pressed = {k: w.keys[k] and not w.data.prev_keys[k] for k in w.data.prev_keys.keys()}
    for k in w.data.prev_keys.keys():
        w.data.prev_keys[k] = w.keys[k]
    
    if pressed['escape']:
        w.stop()
        return

    # 테마 선택 로직
    if not w.data.theme_selected:
        for key in ['1', '2', '3', '4']:
            if pressed[key]:
                w.data.stair_theme = w.data.theme_images[key]
                w.data.theme_selected = True
                w.setText(w.data.info_text, f"테마 {key}번이 선택되었습니다!\n\n'Enter' 키를 눌러 게임 시작!")
        return 

    # 게임 시작 대기 로직
    if not w.data.is_playing:
        if pressed['return']:
            w.data.is_playing = True
            w.data.score = 0
            w.setText(w.data.score_text, "점수: 0")
            w.data.last_move_time = timestamp
            
            # 게임용 UI 요소 표시
            w.hideObject(w.data.info_text)
            w.showObject(w.data.char_id)
            w.showObject(w.data.score_panel)
            w.showObject(w.data.score_text)
            
            w.showObject(w.data.bg_id)
            w.lowerObject(w.data.bg_id)
            
            # 재시작 시 배경 위치 맨 아래(-4800)로 리셋
            w.data.current_bg_y = -4800
            w.moveObject(w.data.bg_id, 0, w.data.current_bg_y)
            
            # 잔여 계단 초기화
            for s in w.data.stairs:
                w.deleteObject(s['rect'])
            w.data.stairs.clear()
            
            # 캐릭터 위치 초기화
            w.data.char_x, w.data.char_y = 400, 353
            w.moveObject(w.data.char_id, w.data.char_x, w.data.char_y)
            
            # 계단 초기화
            start_rect = w.newImage(400, 400, w.data.stair_theme, new_width=30, new_height=20)
            w.data.stairs.append({'rect': start_rect, 'dir': 'none', 'x': 400, 'y': 400})
            
            last_x, last_y = 400, 400
            for _ in range(15):
                stair = generate_stair(last_x, last_y)
                w.data.stairs.append(stair)
                last_x, last_y = stair['x'], stair['y']
                
            raise_ui_and_character()
        return

    # 게임 중단 처리 (백스페이스)
    if pressed['backspace']:
        w.data.is_playing = False
        w.playSound('byebye.mp3') # 죽음/중단 효과음 재생[cite: 2, 9]
        w.setText(w.data.info_text, f"게임이 중단되었습니다!\n최종 점수: {w.data.score}\n\n'Enter' 키를 눌러 다시 시작")
        w.showObject(w.data.info_text)
        return
        
    # 시간 초과 패배 처리
    if timestamp - w.data.last_move_time > 3.0:
        w.data.is_playing = False
        w.playSound('byebye.mp3') # 죽음 효과음 재생[cite: 2, 9]
        w.setText(w.data.info_text, f"3초 초과! 게임 오버.\n최종 점수: {w.data.score}\n\n'Enter' 키를 눌러 다시 시작")
        w.showObject(w.data.info_text)
        raise_ui_and_character()
        return
        
    # 캐릭터 이동 및 치트 로직
    is_auto_playing = w.keys['space']
    
    if pressed['left'] or pressed['right'] or is_auto_playing:
        next_stair = w.data.stairs[1]
        
        player_dir = None
        if is_auto_playing:
            player_dir = next_stair['dir'] 
        elif pressed['left']: 
            player_dir = 'left'
        elif pressed['right']: 
            player_dir = 'right'
            
        # 틀린 방향으로 이동 시 사망
        if player_dir != next_stair['dir']:
            w.data.is_playing = False
            w.playSound('byebye.wav') # 죽음 효과음 재생[cite: 2, 9]
            w.setText(w.data.info_text, f"잘못된 방향! 게임 오버.\n최종 점수: {w.data.score}\n\n'Enter' 키를 눌러 다시 시작")
            w.showObject(w.data.info_text)
            raise_ui_and_character()
            return
            
        # 정상적으로 계단을 오를 때
        w.data.score += 1
        w.setText(w.data.score_text, f"점수: {w.data.score}")
        w.data.last_move_time = timestamp
        
        # 캐릭터 좌표 이동
        w.data.char_x += 30 if player_dir == 'right' else -30
        w.data.char_y -= 20
        w.moveObject(w.data.char_id, w.data.char_x, w.data.char_y)
        
        passed_stair = w.data.stairs.pop(0)
        w.deleteObject(passed_stair['rect'])
                
        last_stair = w.data.stairs[-1]
        w.data.stairs.append(generate_stair(last_stair['x'], last_stair['y']))
        
        raise_ui_and_character()

    # =========================================================
    # [애니메이션 로직] 카메라 스무딩 및 배경 패럴랙스 스크롤
    # =========================================================
    if w.data.is_playing:
        # 1. 캐릭터 부드러운 카메라 추적
        target_char_x, target_char_y = 390, 360
        
        diff_x = target_char_x - w.data.char_x
        diff_y = target_char_y - w.data.char_y
        
        if abs(diff_x) > 0.1 or abs(diff_y) > 0.1:
            shift_x = diff_x * 0.15
            shift_y = diff_y * 0.15
            
            w.data.char_x += shift_x
            w.data.char_y += shift_y
            w.moveObject(w.data.char_id, w.data.char_x, w.data.char_y)
            
            for s in w.data.stairs:
                s['x'] += shift_x
                s['y'] += shift_y
                w.moveObject(s['rect'], s['x'], s['y'])

        # 2. 통짜 배경 스크롤 (-4800에서 시작하여 점수에 따라 0을 향해 올라감)
        target_bg_y = min(-4800 + (w.data.score * 40), 0)
        
        # 보간법을 적용해 부드럽게 배경 스크롤 이동
        w.data.current_bg_y += (target_bg_y - w.data.current_bg_y) * 0.05
        w.moveObject(w.data.bg_id, 0, w.data.current_bg_y)

w = gui.configure(initialize, update, title="무한의 계단", width=800, height=600)
w.start()
