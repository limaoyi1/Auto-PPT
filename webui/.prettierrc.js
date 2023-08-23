/*
 * @Description: prettierrc
 * @Author: Kevin
 * @Date: 2022-04-25 13:41:50
 * @LastEditors: Kevin
 * @LastEditTime: 2022-04-27 09:52:17
 */
module.exports = {
	printWidth: 175, // 每行代码长度（默认175）
	trailingComma: "none", // 在对象或数组最后一个元素后面是否加逗号
	tabWidth: 2, // 每个tab相当于多少个空格（默认2）
	useTabs: true, // 使用tab（制表符）缩进而非空格
	semi: false, // 是否在行尾加分号
	singleQuote: false, // 使用单引号代替双引号
	arrowParens: "avoid", // (x) => {} 箭头函数参数只有一个时是否要有小括号。avoid：省略括号
	bracketSpacing: true, // 在对象，数组括号与文字之间加空格 "{ foo: bar }"
	proseWrap: "preserve", // 默认值。因为使用了一些折行敏感型的渲染器（如GitHub comment）而按照markdown文本样式进行折行
	htmlWhitespaceSensitivity: "ignore", // HTML 文件空格敏感度
	jsxSingleQuote: false, // jsx中是否使用单引号
	endOfLine: "auto", // 结尾是 \n \r \n\r auto
	jsxBracketSameLine: true // 将>多行JSX元素放在最后一行的末尾，而不是单独放在下一行
};
