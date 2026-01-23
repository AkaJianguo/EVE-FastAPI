/**
 * 将 UTC 字符串转换为北京时间格式
 * @param {string} utcString - 如 "2026-01-18T11:01:50Z"
 * @returns {string} - 如 "2026-01-18 19:01:50"
 */
function formatToBeijingTime(utcString) {
    const date = new Date(utcString);

    // 使用 Intl 对象的格式化功能
    const formatter = new Intl.DateTimeFormat('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false, // 使用 24 小时制
        timeZone: 'Asia/Shanghai' // 强制指定北京时区
    });

    // 格式化后的结果通常是 "2026/01/18 19:01:50"
    // 我们将斜杠替换为横杠以符合常用习惯
    return formatter.format(date).replace(/\//g, '-');
}

console.log(formatToBeijingTime("2026-01-18T11:01:50Z")); 
// 输出: 2026-01-18 19:01:50