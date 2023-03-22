const path = require("path");
const rootpath = path.dirname(__dirname); //执行一次dirname将目录定位到docs目录
const utils = require("./utils/index.js");
const filehelper = require("./utils/initPage.js");
const generateBarConfig = function(name) {
  return utils.genSidebar(
    "",
    filehelper.getFileName(rootpath + `/${name}/`, `/${name}/`),
    true
  )
};

// 在这里添加目录
const bars = ['chatgpt', 'rules'];

const sidebar = bars.reduce((accu, current) => {
  accu[`/${current}/`] = generateBarConfig(current);
  return accu;
}, {});

module.exports = {
  base: "/",
  themeConfig: {
    lastUpdated: "Last Updated",
    nav: [
      { text: "和 AI 聊技术", link: "/chatgpt/" },
      { text: "开发规范", link: "/rules/" },
      { text: "Github", link: "https://github.com/hugheschoi" },
    ],
    sidebar,
  },
};
