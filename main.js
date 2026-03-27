// State
let currentCategory = 'animals';
let currentIndex = 0;
let clickCount = 0;
let currentLang = 'zh'; // 'zh', 'en', 'ja'
let cardChangeCounter = 0; // 換景計數器

// 🧼 修正後的純淨吉卜力背景圖庫 (確保每個路徑對應現有實體檔案)
const bgLibrary = {
    animals: ['bg_ghibli_nature.png', 'bg_ghibli_animals.png'],
    vehicles: ['bg_ghibli_road.png', 'bg_ghibli_vehicles.png'],
    ocean: ['bg_ghibli_ocean.png'],
    pets: ['bg_ghibli_room.png', 'bg_ghibli_pets.png'],
    fruits: ['bg_ghibli_fruits.png'],
    dinosaurs: ['bg_ghibli_dinosaurs.png'],
    insects: ['bg_ghibli_insects.png'],
    household: ['bg_ghibli_room.png', 'bg_ghibli_household.png'],
    shapes: ['bg_ghibli_nature.png'],
    numbers: ['bg_ghibli_room.png'],
    letters: ['bg_ghibli_nature.png']
};

// DOM Elements
const startOverlay = document.getElementById('start-overlay');
const startBtn = document.getElementById('start-btn');
const gameApp = document.getElementById('game-app');
const lobbyContainer = document.getElementById('lobby-container');
const gameContainer = document.getElementById('game-container');
const catCards = document.querySelectorAll('.cat-card');
const backBtn = document.getElementById('back-btn');
const btnPrev = document.getElementById('prev-btn');
const btnNext = document.getElementById('next-btn');
const card = document.getElementById('card');
const itemEmoji = document.getElementById('item-emoji');
const itemName = document.getElementById('item-name');
const langBtns = document.querySelectorAll('.lang-btn');
const currentCategoryName = document.getElementById('current-category-name');

// Initialize Game
function initGame() {
    startOverlay.classList.add('hidden');
    gameApp.classList.remove('hidden');
    showLobby();
}

// 顯示大廳
function showLobby() {
    lobbyContainer.classList.remove('hidden');
    gameContainer.classList.add('hidden');
    // 大廳背景使用專屬漸層
    document.body.style.background = `linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)`;
    
    // 刷新大廳文字 (如果切換語言後回來)
    refreshLobbyText();
    twemoji.parse(document.body, { ext: '.svg', folder: 'svg' });
}

// 顯示遊戲畫面
function showGame(category) {
    currentCategory = category;
    lobbyContainer.classList.add('hidden');
    gameContainer.classList.remove('hidden');
    
    // 重設換景計數器
    cardChangeCounter = 0;
    
    // 設定分類名稱標題
    updateCategoryTitle();
    
    // 設定初始背景
    applyBackground(currentCategory);
    
    // 隨機選取該分類的第一張卡片
    if (gameData[currentCategory] && gameData[currentCategory].length > 0) {
        currentIndex = Math.floor(Math.random() * gameData[currentCategory].length);
    } else {
        currentIndex = 0;
    }
    
    updateDisplay();
    // 進入時唸出名稱
    const list = gameData[currentCategory];
    if (list && list[currentIndex]) {
        speak(list[currentIndex]['name_' + currentLang] || list[currentIndex].name_zh || list[currentIndex].name || "");
    }
}

// 更新分類標題
function updateCategoryTitle() {
    const activeCard = Array.from(catCards).find(c => c.getAttribute('data-category') === currentCategory);
    if (activeCard) {
        const title = activeCard.getAttribute('data-name-' + currentLang) || activeCard.getAttribute('data-name-zh');
        currentCategoryName.textContent = title;
    }
}

// 刷新大廳卡片文字
function refreshLobbyText() {
    catCards.forEach(card => {
        const textContent = card.getAttribute('data-name-' + currentLang) || card.getAttribute('data-name-zh');
        const icon = card.innerHTML.split('<br>')[0];
        card.innerHTML = `${icon}<br><span>${textContent}</span>`;
    });
    
    const lobbyTitle = document.getElementById('lobby-title');
    if (lobbyTitle) {
        if (currentLang === 'en') lobbyTitle.textContent = "Pick a theme to explore!";
        else if (currentLang === 'ja') lobbyTitle.textContent = "テーマをえらんでね！";
        else lobbyTitle.textContent = "選擇一個主題開始探索吧！";
    }
}

// 切換背景
function applyBackground(category) {
    const list = bgLibrary[category] || ['bg_ghibli_nature.png'];
    // 隨機挑選一張
    let randomBg = list[Math.floor(Math.random() * list.length)];
    
    // 使用絕對相對路徑確保 GitHub Pages 正確解析
    const bgUrl = `./assets/backgrounds/${randomBg}`;
    const defaultGradient = `linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)`;
    
    document.body.style.background = `url('${bgUrl}') center/cover no-repeat, ${defaultGradient}`;
    document.body.style.backgroundAttachment = 'fixed';
}

// 順序切換
function pickSequentialItem(direction = 'next') {
    const list = gameData[currentCategory];
    if (!list || list.length === 0) return;

    if (direction === 'next') {
        currentIndex = (currentIndex + 1) % list.length;
    } else if (direction === 'prev') {
        currentIndex = (currentIndex - 1 + list.length) % list.length;
    }
    
    // 換景邏輯：每切換 7 次更換一次背景
    cardChangeCounter++;
    if (cardChangeCounter >= 7) {
        applyBackground(currentCategory);
        cardChangeCounter = 0;
    }
    
    updateDisplay();
    speak(list[currentIndex]['name_' + currentLang] || list[currentIndex].name_zh || list[currentIndex].name || "");
}

// 更新卡片畫面
function updateDisplay() {
    const list = gameData[currentCategory];
    const item = list[currentIndex];
    if(!item) return;

    // 擴充 Fallback 機制防止 Undefined
    const textToShow = item['name_' + currentLang] || item.name_zh || item.name || "";
    itemName.textContent = textToShow;
    
    if (item.img) {
        itemEmoji.innerHTML = `<img src="${item.img}" class="custom-card-img" />`;
    } else if (item.emoji) {
        itemEmoji.textContent = item.emoji;
        twemoji.parse(itemEmoji, { ext: '.svg', folder: 'svg' });
    } else {
        itemEmoji.textContent = "❓";
    }
    
    card.style.animation = 'none';
    card.classList.remove('bounce-animation');
}

// 發音引擎
function speak(text) {
    if (!text) return;
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const msg = new SpeechSynthesisUtterance();
        msg.text = text;
        
        if (currentLang === 'en') {
            msg.lang = 'en-US';
            msg.rate = 0.85;
        } else if (currentLang === 'ja') {
            msg.lang = 'ja-JP';
            msg.rate = 0.85;
        } else {
            msg.lang = 'zh-TW';
            msg.rate = 0.9;
        }
        
        msg.pitch = 1.2;
        window.speechSynthesis.speak(msg);
    }
}

// 獎勵紙屑
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

// 語言切換
langBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        currentLang = btn.getAttribute('data-lang');
        langBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // 刷新大廳與標題
        refreshLobbyText();
        updateCategoryTitle();
        
        // 刷新 Welcome 畫面 (如果還看得到)
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

        // 如果在遊戲中，刷新內容並重唸
        if (!gameContainer.classList.contains('hidden')) {
            updateDisplay();
            const list = gameData[currentCategory];
            if(list && list[currentIndex]) {
                speak(list[currentIndex]['name_' + currentLang] || list[currentIndex].name_zh || list[currentIndex].name || "");
            }
        }
        
        twemoji.parse(document.body, { ext: '.svg', folder: 'svg' });
    });
});

// 類別卡片點擊
catCards.forEach(c => {
    c.addEventListener('click', () => {
        const cat = c.getAttribute('data-category');
        showGame(cat);
    });
});

// 返回按鈕
backBtn.addEventListener('click', showLobby);

// 滑動更換
let isAnimating = false;
function changeItemWithSlide(direction) {
    if (isAnimating) return;
    isAnimating = true;

    const outAnimation = direction === 'next' ? 'slideOutLeft 0.3s ease forwards' : 'slideOutRight 0.3s ease forwards';
    card.style.animation = outAnimation;

    setTimeout(() => {
        pickSequentialItem(direction);
        card.style.animation = 'none';
        void card.offsetWidth;
        const inAnimation = direction === 'next' ? 'slideInRight 0.3s ease forwards' : 'slideInLeft 0.3s ease forwards';
        card.style.animation = inAnimation;
        
        setTimeout(() => {
            isAnimating = false;
        }, 300);
    }, 300);
}

btnPrev.addEventListener('click', () => changeItemWithSlide('prev'));
btnNext.addEventListener('click', () => changeItemWithSlide('next'));

// 卡片點擊互動
card.addEventListener('click', () => {
    if (isAnimating) return;
    const list = gameData[currentCategory];
    const item = list[currentIndex];
    speak(item['name_' + currentLang] || item.name_zh || item.name || "");
    clickCount++;
    card.style.animation = 'none';
    card.classList.remove('bounce-animation');
    void card.offsetWidth;
    card.classList.add('bounce-animation');
    if (clickCount % 5 === 0) triggerReward();
});

// 手勢支援
let touchStartX = 0;
let touchEndX = 0;
card.addEventListener('touchstart', e => { touchStartX = e.changedTouches[0].screenX; }, { passive: true });
card.addEventListener('touchend', e => {
    touchEndX = e.changedTouches[0].screenX;
    if (touchStartX - touchEndX > 50) changeItemWithSlide('next');
    else if (touchEndX - touchStartX > 50) changeItemWithSlide('prev');
});

// 鍵盤支援
document.addEventListener('keydown', (e) => {
    if (!startOverlay.classList.contains('hidden')) {
        if (e.key === 'Enter' || e.key === ' ') startBtn.click();
        return;
    }
    if (!gameContainer.classList.contains('hidden')) {
        if (e.key === 'ArrowRight') changeItemWithSlide('next');
        else if (e.key === 'ArrowLeft') changeItemWithSlide('prev');
        else if (e.key === 'Enter' || e.key === ' ') card.click();
        else if (e.key === 'Escape') backBtn.click();
    }
});
