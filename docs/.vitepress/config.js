const fs = require("fs");
const path = require("path");
console.log(process.env.NODE_ENV);
const docsPath = path.dirname(__dirname); // docs 目录路径
const sidebarConfig = generateSidebarConfig(docsPath);
// console.log(JSON.stringify(sidebarConfig, null, 2));
/**
 * 根据 docs 目录生成 VitePress 的 sidebar 配置
 * @param {string} docsPath - docs 目录路径
 * @returns {object} sidebar 配置
 */
function generateSidebarConfig(docsPath, link = '', index = 0) {
  const sidebarConfig = {};
  const files = fs.readdirSync(docsPath);

  files.forEach((filename) => {
    if (filename.startsWith(".")) return;
    const filepath = path.join(docsPath, filename);
    const stat = fs.statSync(filepath);
    // 如果是文件夹，则递归生成子级 sidebar 配置
    if (stat.isDirectory()) {
      if (index === 0) {
        const config = generateSidebarConfig(filepath, `/${filename}/`, index + 1);
        if (!sidebarConfig[`/${filename}/`]) {
          sidebarConfig[`/${filename}/`] = [config];
        }
      } else {
        if (!sidebarConfig.items) {
          sidebarConfig.items = [];
        }
        sidebarConfig.items.push(generateSidebarConfig(filepath, `${link}${filename}/`, index + 1))
      }
    } else {
      // // 如果是文件，则添加到当前级别的 sidebar 配置中
      const extname = path.extname(filepath);
      const basename = path.basename(filepath, extname);
      if (filename === 'index.md' && index > 0) {
        const menuPath = path.dirname(filepath);
        const menuName = path.basename(menuPath) 
        sidebarConfig.text = menuName;
        sidebarConfig.link = link;
      }
      if (extname === ".md" && filename !== "index.md") {
        if (!sidebarConfig.items) {
          sidebarConfig.items = [];
        }
        sidebarConfig.items.push({
          text: basename,
          link: `${link}${basename}`,
        });
      }
    }
  });

  return sidebarConfig;
}

if (process.env.NODE_ENV === 'production') {
  delete sidebarConfig.algorithm;
}

module.exports = {
  base: "/",
  themeConfig: {
    lastUpdated: "Last Updated",
    nav: [
      { text: "和 AI 聊技术", link: "/chatgpt/" },
      { text: "开发规范", link: "/rules/" },
      { text: "算法", link: "/algorithm/" },
      { text: "Github", link: "https://github.com/hugheschoi" },
    ],
    sidebar: sidebarConfig,
  },
};

/**
 * {
  "/chatgpt/": [
    {
      "text": "",
      "items": [
        {
          "text": "位运算及其应用",
          "link": "/chatgpt/位运算及其应用"
        }
      ],
      "collapsable": true,
      "sidebarDepth": 2
    }
  ],
  "/rules/": [
    {
      "text": "",
      "items": [
        {
          "text": "husky",
          "link": "/rules/husky"
        },
        {
          "text": "分支管理规范",
          "link": "/rules/分支管理规范"
        }
      ],
      "collapsable": true,
      "sidebarDepth": 2
    }
  ],
  "/algorithm/": [
    {
      "text": "",
      "items": [
        {
          "text": "array",
          "link": "/basic/array"
        }
      ],
      "collapsable": true,
      "sidebarDepth": 2
    }
  ]
}
 */
