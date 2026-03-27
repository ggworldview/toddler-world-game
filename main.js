// State
let currentCategory = 'animals';
let currentIndex = 0;
let clickCount = 0;
let currentLang = 'zh'; // 'zh', 'en', 'ja'
let cardChangeCounter = 0; // 換景計數器

// 🧼 完美擴張後的吉卜力背景圖庫 (20張大師級場景)
const bgLibrary = {
    animals: ['bg_ghibli_animals.png', 'bg_ghibli_nature.png', 'bg_ghibli_mountain.png'],
    vehicles: ['bg_ghibli_vehicles.png', 'bg_ghibli_road.png', 'bg_ghibli_construction.png', 'bg_ghibli_city.png'],
    ocean: ['bg_ghibli_ocean.png', 'bg_ghibli_underwater.png'],
    pets: ['bg_ghibli_room.png', 'bg_ghibli_pets.png', 'bg_ghibli_household.png'],
    fruits: ['bg_ghibli_fruits.png', 'bg_ghibli_nature.png'],
    dinosaurs: ['bg_ghibli_dinosaurs.png', 'bg_ghibli_mountain.png', 'bg_ghibli_desert.png'],
    insects: ['bg_ghibli_insects.png', 'bg_ghibli_nature.png'],
    household: ['bg_ghibli_household.png', 'bg_ghibli_room.png'],
    shapes: ['bg_ghibli_nature.png', 'bg_ghibli_statue.png'],
    numbers: ['bg_ghibli_room.png', 'bg_ghibli_taipei101.png'],
    letters: ['bg_ghibli_nature.png', 'bg_ghibli_fuji.png'],
    // 額外混合場景
    winter: ['bg_ghibli_snow.png']
};

// 特殊類別對應 (針對特定主題加強)
const categoryBgs = {
    'ocean': ['bg_ghibli_ocean.png', 'bg_ghibli_underwater.png'],
    'dinosaurs': ['bg_ghibli_dinosaurs.png', 'bg_ghibli_desert.png', 'bg_ghibli_mountain.png'],
    'vehicles': ['bg_ghibli_vehicles.png', 'bg_ghibli_road.png', 'bg_ghibli_construction.png', 'bg_ghibli_taipei101.png', 'bg_ghibli_city.png', 'bg_ghibli_statue.png', 'bg_ghibli_fuji.png']
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
    // 大廳背景使用平和的暖白色或輕盈漸層
    document.body.style.background = `#f7f7f7`;
    document.body.style.backgroundImage = `linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%)`;
    
    refreshLobbyText();
    twemoji.parse(document.body, { ext: '.svg', folder: 'svg' });
}

// 顯示遊戲畫面
function showGame(category) {
    currentCategory = category;
    lobbyContainer.classList.add('hidden');
    gameContainer.classList.remove('hidden');
    
    cardChangeCounter = 0;
    updateCategoryTitle();
    applyBackground(currentCategory);
    
    if (gameData[currentCategory] && gameData[currentCategory].length > 0) {
        currentIndex = Math.floor(Math.random() * gameData[currentCategory].length);
    } else {
        currentIndex = 0;
    }
    
    updateDisplay();
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

// 切換背景 (徹底移除藍色底，僅留米白色緩衝底)
function applyBackground(category) {
    // 優先從分類對應庫中選取，若無則從大庫隨機選取
    const list = categoryBgs[category] || bgLibrary[category] || ['bg_ghibli_nature.png'];
    let randomBg = list[Math.floor(Math.random() * list.length)];
    
    // 增加雪地機制 (如果是數字或字母，偶爾出雪景)
    if ((category === 'numbers' || category === 'letters') && Math.random() > 0.7) {
        randomBg = 'bg_ghibli_snow.png';
    }

    const bgUrl = `./assets/backgrounds/${randomBg}`;
    // 移除藍底，改用純色背景作為緩衝，視覺更純淨
    document.body.style.background = `url('${bgUrl}') center/cover no-repeat, #f7f7f7`;
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
        
        refreshLobbyText();
        updateCategoryTitle();
        
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
