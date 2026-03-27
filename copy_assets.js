const fs = require('fs');
const path = require('path');

const srcDir = `C:\\Users\\ggwor\\.gemini\\antigravity\\brain\\6577c61b-ddd4-414b-a22a-8a0bcbe63f70`;
const destDir = path.join(__dirname, 'assets');

if (!fs.existsSync(destDir)) fs.mkdirSync(destDir);

const files = fs.readdirSync(srcDir);
files.forEach(file => {
    if (file.startsWith('dino_') || file.startsWith('insect_')) {
        const cleanName = file.replace(/_\d+\.png$/, '.png');
        if (cleanName.endsWith('.png')) {
            fs.copyFileSync(path.join(srcDir, file), path.join(destDir, cleanName));
            console.log('Copied:', cleanName);
        }
    }
});
