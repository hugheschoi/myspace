const utils = {
  genSidebar: function (text, items = [''], collapsable = false, sidebarDepth = 2) {
    var arr = new Array();
    arr.push({
      text,
      items,
      collapsable,
      sidebarDepth
    })
    return arr;
  }
};

module.exports = utils;