// State
let currentCategory = 'animals';
let currentIndex = 0;
let clickCount = 0;

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
    fruits: ['bg_kitchen.png', 'bg_farm.png', 'bg_garden.png', 'bg_plains.png']
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

// Initialize Game
function initGame() {
    startOverlay.classList.add('hidden');
    gameContainer.classList.remove('hidden');
    
    // 初始化發聲 (解鎖瀏覽器音效)
    speak('開始隨機大冒險！');
    
    // 設定初始背景與畫面
    applyBackground(currentCategory);
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
    speak(list[currentIndex].name);
}

// 更新卡片畫面
function updateDisplay() {
    const list = gameData[currentCategory];
    const item = list[currentIndex];
    
    if(!item) return;

    itemName.textContent = item.name;
    
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
        msg.lang = 'zh-TW'; // 設定為中文台灣
        msg.rate = 0.9; // 語速稍微放慢適合幼兒
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
        
        // 切換類別時，將索引歸零，從第一張開始順序看
        currentIndex = 0;
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
    speak(item.name);
    
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
