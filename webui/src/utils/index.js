/**
 * description： 工具函数
 * @author Kevin
 * @date 2023/8/10
 */
import _ from "lodash"
const short = require('short-uuid');

const utils = {
	md2json: function (){

	},
	json2md: function (){

	},
	/**
	 * 展平数组转目录树
	 * @param data
	 */
	flattenToTree: function (data){
		let map = {};
		for(let item of data){
			map[item.id] = item
		}
		let result = []; //存放数组
		for(let item of data){
			item.children = []; //给每个数组添加一个空children
			if(item.parentId === null){
				result.push(item)//最上级的标签
			}else{
				//相当于用这个 parentId 当做父Id去查找对比查找数据
				let parent = map[item.parentId]
				//添加到刚刚定义children数组中去
				parent.children.push(item)
			}
		}
		return result
	},
	/**
	 * markdown的str转 目录树形结构
	 */
	parseMarkdownToTree:function (markdown){
		const lines = markdown.split('\n');
		const directoryTree = [];
		let currentSection = { type: 'root', children: directoryTree };
		const listStack = [];

		for (const line of lines) {
			const trimmedLine = line.trim();
			const matchHeading = trimmedLine.match(/^(#{1,6})\s+(.*)/);
			const matchListItem = trimmedLine.match(/^(\s*[-+*])\s+(.*)/);
			const matchImage = trimmedLine.match(/^!\[([^\]]+)\]\(([^\)]+)\)/);

			if (matchHeading) {
				const level = matchHeading[1].length;
				const text = matchHeading[2];
				const newSection = { type: 'section', level, text, children: [], id: short.generate() };
				while (listStack.length > 0 && listStack[listStack.length - 1].level >= newSection.level) {
					listStack.pop();
				}
				if (listStack.length === 0) {
					directoryTree?.push(newSection);
				} else {
					listStack[listStack.length - 1].children?.push(newSection);
				}
				listStack?.push(newSection);
				currentSection = newSection;
			} else if (matchListItem) {
				const text = matchListItem[2];
				if (currentSection.type !== 'list') {
					const newList = { type: 'list', level: matchListItem[1].length, children: [], id: short.generate() };
					currentSection.children?.push(newList);
					listStack?.push(currentSection);
					currentSection = newList;
				}
				const newItem = { type: 'listItem', text, children: [], id: short.generate() };
				currentSection.children?.push(newItem);
			} else if (matchImage) {
				const altText = matchImage[1];
				const src = matchImage[2];
				currentSection?.type === "list" ? listStack[listStack.length - 1].children?.push({
					type: 'image',
					altText,
					src,
					id: short.generate()
				}) : currentSection.children?.push({type: 'image', altText, src, id: short.generate()});
			} else if (trimmedLine !== '') {
				if (currentSection.type === 'list') {
					const newParagraph = { type: 'paragraph', text: trimmedLine, id: short.generate() };
					listStack[listStack.length - 1].children?.push(newParagraph);
				} else {
					currentSection.children?.push({ type: 'paragraph', text: trimmedLine, id: short.generate() });
				}
			}
		}

		return directoryTree;
	},
}

export default utils

