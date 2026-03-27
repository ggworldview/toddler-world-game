// State
let currentCategory = 'animals';
let currentIndex = 0;
let clickCount = 0;
let currentLang = 'zh'; // 'zh', 'en', 'ja'

// ====== 新增多重場景圖庫 (預留給未來 AI 宮崎駿算圖) ======
const bgLibrary = {
    animals: ['bg_savanna.png', 'bg_forest.png', 'bg_desert.png', 'bg_plains.png'],
    vehicles: ['bg_airport.png', 'bg_city.png', 'bg_farm.png', 'bg_highway.png'],
    insects: ['bg_leaf.png', 'bg_garden.png', 'bg_treetrunk.png'],
    dinosaurs: ['bg_volcano.png', 'bg_jungle.png', 'bg_river.png'],
    shapes: ['bg_pastel.png', 'bg_chalkboard.png', 'bg_starry.png'],
    numbers: ['bg_classroom.png', 'bg_math.png'],
    letters: ['bg_library.png', 'bg_nursery.png'],
    household: ['bg_livingroom.png', 'bg_bedroom.png', 'bg_kitchen.png'],
    fruits: ['bg_kitchen.png', 'bg_farm.png', 'bg_garden.png', 'bg_plains.png'],
    pets: ['bg_livingroom.png', 'bg_garden.png'],
    ocean: ['bg_beach.png', 'bg_river.png', 'bg_underwater.png']
};

// DOM Elements
const startOverlay = document.getElementById('start-overlay');
const startBtn = document.getElementById('start-btn');
const gameContainer = document.getElementById('game-container');
const tabBtns = document.querySelectorAll('.tab-btn');
const btnPrev = document.getElementById('prev-btn');
const btnNext = document.getElementById('next-btn');
const card = document.getElementById('card');
const itemEmoji = document.getElementById('item-emoji');
const itemName = document.getElementById('item-name');
const langBtns = document.querySelectorAll('.lang-btn');

// Initialize Game
function initGame() {
    startOverlay.classList.add('hidden');
    gameContainer.classList.remove('hidden');
    
    // 設定初始背景與畫面
    applyBackground(currentCategory);
    
    // 遊戲開始時，隨機選取第一張卡片
    if (gameData[currentCategory] && gameData[currentCategory].length > 0) {
        currentIndex = Math.floor(Math.random() * gameData[currentCategory].length);
    }
    pickSequentialItem('none');
    
    // 初始進入先掃描將畫面的分類標籤繪本化
    twemoji.parse(document.body, { ext: '.svg', folder: 'svg' });
}

// 切換背景
function applyBackground(category) {
    const list = bgLibrary[category] || ['bg_default.jpg'];
    const randomBg = list[Math.floor(Math.random() * list.length)];
    
    // 預設漸層色作為佔位符：等冷卻時間結束把圖畫出來放入資料夾後，照片就會自動覆蓋展現出來！
    const defaultGradient = `linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)`;
    document.body.style.background = `url('./assets/backgrounds/${randomBg}') center/cover no-repeat, ${defaultGradient}`;
}

// 順序切換下一個/上一個項目 (取代舊有的隨機模式)
function pickSequentialItem(direction = 'next') {
    const list = gameData[currentCategory];
    if (list.length === 0) return;

    if (direction === 'next') {
        currentIndex = (currentIndex + 1) % list.length;
    } else if (direction === 'prev') {
        currentIndex = (currentIndex - 1 + list.length) % list.length;
    } else {
        // Init state (keep current index, usually 0)
    }
    
    updateDisplay();
    speak(list[currentIndex]['name_' + currentLang] || list[currentIndex].name_zh);
}

// 更新卡片畫面
function updateDisplay() {
    const list = gameData[currentCategory];
    const item = list[currentIndex];
    
    if(!item) return;

    // 根據目前的語系狀態，顯示對應的名稱
    const textToShow = item['name_' + currentLang] || item.name_zh;
    itemName.textContent = textToShow;
    
    if (item.img) {
        // 採用直接掛載透明背板照片的模式
        itemEmoji.innerHTML = `<img src="${item.img}" class="emoji" />`;
    } else {
        // 採用 Twemoji 解析模式
        itemEmoji.textContent = item.emoji;
        twemoji.parse(itemEmoji, { ext: '.svg', folder: 'svg' });
    }
    
    // 移除動畫以便下次點擊能夠重新觸發
    card.style.animation = 'none';
    card.classList.remove('bounce-animation');
}

// Ensure TTS works
function speak(text) {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel(); // 停止先前的語音
        const msg = new SpeechSynthesisUtterance();
        msg.text = text;
        
        // 根據國籍切換最佳發音引擎配置
        if (currentLang === 'en') {
            msg.lang = 'en-US';
            msg.rate = 0.85; // 英文稍微放慢聽得更清楚
        } else if (currentLang === 'ja') {
            msg.lang = 'ja-JP';
            msg.rate = 0.85;
        } else {
            msg.lang = 'zh-TW';
            msg.rate = 0.9;
        }
        
        msg.pitch = 1.2; // 語調稍微提高比較活潑
        window.speechSynthesis.speak(msg);
    }
}

// Trigger Confetti (移除文字，只留下純粹彩色紙屑)
function triggerReward() {
    confetti({
        particleCount: 150,
        spread: 80,
        origin: { y: 0.6 },
        colors: ['#ff006e', '#ffbe0b', '#fb5607', '#8338ec', '#3a86ff']
    });
}

// Event Listeners
startBtn.addEventListener('click', initGame);

// 註冊語言切換
langBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        currentLang = btn.getAttribute('data-lang');
        
        // 更新 UI active 狀態
        langBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // 全域刷新 Tabs 文字
        tabBtns.forEach(tb => {
            const textContent = tb.getAttribute('data-name-' + currentLang) || tb.getAttribute('data-name-zh');
            const icon = tb.innerHTML.split(' ')[0]; // 擷取前端的 emoji
            tb.innerHTML = `${icon} ${textContent}`;
        });
        
        // 全域刷新 Welcome 文字
        const welcomeText = document.getElementById('welcome-text');
        if (welcomeText) {
            if (currentLang === 'en') welcomeText.textContent = "Welcome to Menglan's Colorful World";
            else if (currentLang === 'ja') welcomeText.textContent = "モンランのカラフルな世界へようこそ";
            else welcomeText.textContent = "歡迎來到萌嵐的五彩繽紛的世界";
        }
        
        const startBtnElem = document.getElementById('start-btn');
        if (startBtnElem) {
            if (currentLang === 'en') startBtnElem.textContent = "Let's Play!";
            else if (currentLang === 'ja') startBtnElem.textContent = "あそぼう！";
            else startBtnElem.textContent = "開始玩囉！";
        }
        
        // 刷新當前卡片顯示內容
        updateDisplay();
        
        // 如果已經進入遊戲，直接發音新預設語言
        if (!gameContainer.classList.contains('hidden')) {
            const list = gameData[currentCategory];
            if(list && list[currentIndex]) {
                speak(list[currentIndex]['name_' + currentLang] || list[currentIndex].name_zh);
            }
        }
    });
});

// 註冊所有標籤按鈕的點擊事件
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        // 設定分類
        currentCategory = btn.getAttribute('data-category');
        
        // 更新 UI active 狀態
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // 變更背景
        applyBackground(currentCategory);
        
        // 切換類別時，改為隨機抽取該分類的新起點
        if (gameData[currentCategory] && gameData[currentCategory].length > 0) {
            currentIndex = Math.floor(Math.random() * gameData[currentCategory].length);
        } else {
            currentIndex = 0;
        }
        pickSequentialItem('none');
    });
});

// 滑動動畫鎖定狀態
let isAnimating = false;

// 滑動更換項目
function changeItemWithSlide(direction) {
    if (isAnimating) return;
    isAnimating = true;

    // 設定離場動畫
    const outAnimation = direction === 'next' ? 'slideOutLeft 0.3s ease forwards' : 'slideOutRight 0.3s ease forwards';
    card.style.animation = outAnimation;

    // 離場動畫結束後，換圖並進場
    setTimeout(() => {
        pickSequentialItem(direction); // 自動順序翻頁並更新
        
        // 設定進場動畫
        card.style.animation = 'none';
        void card.offsetWidth; // Trigger reflow
        const inAnimation = direction === 'next' ? 'slideInRight 0.3s ease forwards' : 'slideInLeft 0.3s ease forwards';
        card.style.animation = inAnimation;
        
        setTimeout(() => {
            isAnimating = false;
        }, 300);
    }, 300);
}

// 前一個/後一個按鈕
btnPrev.addEventListener('click', () => changeItemWithSlide('prev'));
btnNext.addEventListener('click', () => changeItemWithSlide('next'));

// Card Interaction (點擊卡片彈跳並發聲)
card.addEventListener('click', () => {
    // 稍微防止滑動中點擊
    if (isAnimating) return;

    const list = gameData[currentCategory];
    const item = list[currentIndex];
    
    // 唸出名稱
    speak(item['name_' + currentLang] || item.name_zh);
    
    // 增加點擊次數
    clickCount++;
    
    // 清除 inline 的滑動動畫，改用 class 觸發彈跳
    card.style.animation = 'none';
    card.classList.remove('bounce-animation');
    void card.offsetWidth; // Trigger reflow
    card.classList.add('bounce-animation');
    
    // 檢查獎勵 (每5次)
    if (clickCount % 5 === 0) {
        triggerReward();
    }
});

// 手機滑動操作 (Swipe Handling)
let touchStartX = 0;
let touchEndX = 0;

card.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].screenX;
}, { passive: true });

card.addEventListener('touchend', e => {
    touchEndX = e.changedTouches[0].screenX;
    
    // 如果滑動距離大於 50px 才判定為左右切換，否則保留給原本的點擊發音
    if (touchStartX - touchEndX > 50) {
        changeItemWithSlide('next'); // 往左滑 = 下一頁
    } else if (touchEndX - touchStartX > 50) {
        changeItemWithSlide('prev'); // 往右滑 = 上一頁
    }
});

// 註記鍵盤輔助操作
document.addEventListener('keydown', (e) => {
    // 如果還在開始畫面，按下 Enter 或空白鍵可以直接進入
    if (!startOverlay.classList.contains('hidden')) {
        if (e.key === 'Enter' || e.key === ' ') {
            startBtn.click();
        }
        return;
    }

    // 遊戲畫面操作
    if (e.key === 'ArrowRight') {
        changeItemWithSlide('next');
    } else if (e.key === 'ArrowLeft') {
        changeItemWithSlide('prev');
    } else if (e.key === 'Enter' || e.key === ' ') {
        card.click();
    }
});
