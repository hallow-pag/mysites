

    var cv = document.getElementById('cv');
var c = cv.getContext('2d');
var txtDiv = document.getElementById('txt');
var fileBtn = document.getElementById("up-button");
var img = new Image();
img.src = 'abn.jpg';
img.onload = init; // 图片加载完开始转换
fileBtn.onchange = getImg;

// 根据灰度生成相应字符 MNHQ&OC?7>!:-;.
function toText(g) {
    if (g <= 17) {
        return 'M';
    } else if (g > 17 && g <= 34) {
        return 'N';
    } else if (g > 34 && g <= 51) {
        return 'H';
    } else if (g > 51 && g <= 68) {
        return 'Q';
    } else if (g > 68 && g <= 85) {
        return '&';
    } else if (g > 85 && g <= 102) {
        return 'O';
    } else if (g > 102 && g <= 119) {
        return 'C';
    } else if (g > 119 && g <= 136) {
        return '?';
    } else if (g > 136 && g <= 153) {
        return '7';
    } else if (g > 153 && g <= 170) {
        return '>';
    } else if (g > 170 && g <= 187) {
        return '!';
    } else if (g > 187 && g <= 204) {
        return ':';
    } else if (g > 204 && g <= 221) {
        return '-';
    } else if (g > 221 && g <= 238) {
        return ';';
    }  else {
        return '.';
    }
}


// 根据rgb值计算灰度
function getGray(r, g, b) {
    return 0.299 * r + 0.578 * g + 0.114 * b;
}

// 转换
function init() {
    txtDiv.style.width = img.width + 'px';
    cv.width = img.width;
    cv.height = img.height;
    c.drawImage(img, 0, 0);
    var imgData = c.getImageData(0, 0, img.width, img.height);
    var imgDataArr = imgData.data;
    var imgDataWidth = imgData.width;
    var imgDataHeight = imgData.height;
    var specific = imgDataHeight/imgDataWidth
    var html = '';
    for (h = 0; h < imgDataHeight; h+=14) {
        var p = '<p>';
        for (w = 0; w < imgDataWidth; w+=8) {
            var index = (w + imgDataWidth * h) * 4;
            var r = imgDataArr[index + 0];
            var g = imgDataArr[index + 1];
            var b = imgDataArr[index + 2];
            var gray = getGray(r, g, b);
            p += toText(gray);
        }
        p += '</p>';
        html += p;
    }
    txtDiv.innerHTML = html;
}

// 获取图片
function getImg(file) {
    var reader = new FileReader();
    reader.readAsDataURL(fileBtn.files[0]);
    reader.onload = function () {
        img.src = reader.result;
    }
}

