import mdStr from "@/mocks/markdown"
import "./index.scss"
import {useEffect, useRef, useState} from "react";
import {fromMarkdown} from 'mdast-util-from-markdown'
import {toMarkdown} from "mdast-util-to-markdown"
import {toHtml} from 'hast-util-to-html'
import {toHast} from 'mdast-util-to-hast'
import _ from "lodash"
import {useClickAway} from 'ahooks';
import pptxgen from "pptxgenjs";
import utils from "../../utils";
import WebPptx from "@comp/web-pptx";

const short = require('short-uuid');
let pres;

/**
 * description： 首页
 * @author Kevin
 * @date 2023/8/10
 */
function Home() {
	const tree = utils.parseMarkdownToTree(mdStr) || []
	console.log(tree, "===========tree=========")
	const [leftData, setLeftData] = useState(tree)
	const [rightData, setRightData] = useState(tree)
	const [html, setHtml] = useState(null)
	const ref = useRef(null)
	

	/**
	 * useEffect
	 */
	useEffect(() => {
		initData();
	}, [])
	useEffect(() => {
		initPres();
	}, [])

	/**
	 * useClickAway 点击
	 */
	useClickAway(() => {
	
	}, ref);

	// const

	/**
	 * 初始化数据
	 */
	const initData = () => {
		const tree = fromMarkdown(mdStr)
		renderHtml(tree)
	}

	/**
	 * 实例化pres
	 */
	const initPres = () => {
		pres = new pptxgen();
		return pres
	}

	/**
	 * 生成全部幻灯片
	 */
	const renderAllSlide = () => {
		!_.isEmpty(rightData) && renderSlide(rightData)
	}
	/**
	 * 递归绘制幻灯片
	 * 1、封面和目录要单独绘制
	 * 2、递归渲染到倒数第二级，最后一级和父标题组成一张幻灯片
	 * 3、gpt生成的每小节字数是不确定的，按照 0-80字符/80以上字符 字体大小分为2档，防止字体太多出幻灯片边界，字体太少显得空泛
	 * 4、图片暂时放在左侧50%或者右侧50%，gpt生成内容不确定，很难做成极其通用的，后期按风格或分类做几套模板或者布局（纯体力活）
	 */
	const renderSlide = tree => {
		_.map(tree, o => {
			if (o.level && o.type==="section" && o.level === 1) {  //渲染封面和目录
				renderCover(o)
				renderDirectory(o.children)
			} else {  //渲染除封面/目录外的幻灯片（PS：只渲染至倒数第二级）
				(!_.isEmpty(o.children) && o.type !== "list")  && renderChildSlide(o)
			}
			if(!_.isEmpty(o.children) && o.type !== "list"){
				return renderSlide(o.children)
			}
		})
	}
	/**
	 * 绘制pptx封面
	 */
	const renderCover = item => {
		let slide = pres.addSlide();
		slide.background = {path: 'https://assets.mindshow.fun/themes/greenblue_countryside_vplus_20230720/Cover-bg.jpg'}
		slide.addText(_.get(item, 'text'), {
			x: 0, y: '40%', w: "100%", color: "#666", fontSize: 64, align: "center"});
	}
	/**
	 * 绘制目录界面
	 */
	const renderDirectory = directoryData => {
		console.log("========绘制目录界面===========")
		let slide = pres.addSlide();
		slide.background = {path: 'https://assets.mindshow.fun/themes/greenblue_countryside_vplus_20230720/Cover-bg.jpg'}
		slide && slide.addText("目录", {
			x: "9%", y: '10%', w: "80%", h: "80%", color: "#666", fontSize: 30, valign: "top"
		});
		slide.addText(_.map(directoryData || [], o => ({text: o.text, options: {breakLine: true}})),
			{x: "10%", y: "24%", w: 8.5, h: 2.0, margin: 0.1}
		);
	}
	/**
	 * 绘制底层幻灯
	 * @param item
	 */
	const renderChildSlide = item => {
		let slide = pres.addSlide();
		slide.background = {path: 'https://assets.mindshow.fun/themes/greenblue_countryside_vplus_20230720/Cover-bg.jpg'}
		slide && slide.addText(_.get(item, 'text'), {
			x: "9%", y: '10%', w: "80%", h: "80%", color: "#666", fontSize: 30, valign: "top"
		});
		let itemChild = item?.children || []
		if (!_.isEmpty(itemChild)) {
			let textCount = 0;
			let idx = _.findIndex(itemChild, o => o.type === "list");
			let children = []
			if(_.isNumber(idx)){
				children = flattenDepthOne(itemChild);
			}
			let textList = _.map(_.filter(children, o => o.text), o => {
				textCount += _.size(o.text);
				return ({text: o.text, options: {breakLine: true, bullet: o.type === "listItem"}})
			}) || [];
			let imgUrl = _.get(_.find(children, o => o.type === 'image'), 'src');
			slide && slide.addText(textList, {
				x: "10%",
				y: "24%",
				w: imgUrl ? 4.8 : 8.5,
				h: textCount > 160 ? 3.0 : textCount > 120 ? 2.5 : 2.0,
				margin: 0.1,
				fontSize: textCount > 160 ? 10 : textCount > 80 ? 14 : 20,
				paraSpaceBefore: 2,
				paraSpaceAfter: 4,
			});
			imgUrl && slide.addImage({path: imgUrl, x: "60%", w: "40%", h: "100%", type: "cover"})
		}
	}
	/***
	 * 展平数组
	 */
	const flattenDepthOne = list => {
		let newList = [];
		_.map(list, o => {
			if (o.type === "list" && !_.isEmpty(o?.children)) {
				newList = _.concat([], newList, o?.children)
			}
			newList.push(o);
		})
		return newList
	}
	/**
	 * 导出pptx至本地
	 */
	const exportPptx = () => {
		renderAllSlide()
		pres.writeFile({fileName: "AIGC-PPTX.pptx"});
		console.log("执行导出pptx")
		// pres.write("base64")
		// 	.then((data) => {
		// 		console.log("write as base64: Here are 0-100 chars of `data`:\n");
		// 		console.log(data.substring(0, 100));
		// 		console.log(data)
		// 	})
		// 	.catch((err) => {
		// 		console.error(err);
		// 	});
	}
	/**
	 * 根据左侧的编辑 - 渲染最新的html
	 */
	const renderHtml = mdast => {
		const hast = toHast(mdast)
		const lastHtml = toHtml(hast)
		setHtml(lastHtml)
	}
	/**
	 * 编辑左侧目录树
	 */
	const handleEditMd = (e, idx, id) => {
		const value = e.target.textContent;
		if (value === "") {
			removeItem(e, idx)
			return
		}
		let oldData = _.cloneDeep(rightData)
		let newData = setTreeData(oldData, value, id,"edit")
		setRightData(newData)
	}
	/**
	 * 编辑左侧目录树
	 * @param treeData
	 * @param value
	 * @param id
	 * @param type
	 * @returns {unknown[]}
	 */
	const setTreeData = (treeData, value, id, type) => {
		return _.map(treeData, o=>{
			if(o.id === id){
				if (type === "edit") { //编辑
					o.text = value
				} else if (type === "show") {  //显示操作模块
					o.showOptions = !o.showOptions
				}
			}
			o.children = setTreeData(o?.children, value, id, type)
			return o;
		})
	}
	/**
	 * 操作目录树节点
	 */
	const operateTreeData = (treeData, item, idx, type) =>{
		let isMatch = false
		_.map(treeData, o=>{
			if(!o){
				return
			}
			if(o?.id === item?.id){
				isMatch = true;
				if(type === "add"){
					treeData?.splice(idx + 1, 0, _.cloneDeep({...item, text: " ", children: [],showOptions: false, id: short.generate()}));
					setTreeData(treeData, item?.text, item?.id, "show")
				} else if(type === "addChild"){
					if (_.isEmpty(o.children)) o.children = []
					let neeItem = o.children[o.children?.length -1]
					o.children.push({...neeItem, text: " ", children: [], id: short.generate()})
					setTreeData(treeData, item?.text, item?.id, "show")
				} else if(type === "remove"){
					setTreeData(treeData, item?.text, item?.id, "show")
					treeData?.splice(idx, 1);
				}
			} else {
				o.children = !_.isEmpty(o?.children) ? operateTreeData(o?.children, item, idx, type) : []
				return o;
			}
		})
		return treeData
	}
	/**
	 * 显示options
	 */
	const showOptions = id => {
		let oldData = _.cloneDeep(rightData)
		let newData = setTreeData(oldData, null, id, "show")
		setLeftData(newData)
		setRightData(newData)
	}
	/**
	 * 添加节点
	 * @param item
	 * @param idx
	 */
	const addItem = (item, idx) => {
		operateTree(item, idx, "add")
	}
	/**
	 * 添加子节点
	 * @param item
	 * @param idx
	 */
	const addChildItem = (item, idx) => {
		operateTree(item, idx, "addChild")
	}
	/**
	 * 删除节点
	 * @param item
	 * @param idx
	 */
	const removeItem = (item, idx) => {
		operateTree(item, idx, "remove")
	}
	/**
	 * 操作树节点（新增节点/新增子节点/删除节点）
	 * @param item
	 * @param idx
	 * @param type
	 */
	const operateTree = (item, idx, type) =>{
		let oldData = _.cloneDeep(rightData)
		let newData = operateTreeData(oldData, item, idx, type)
		setLeftData(newData)
		setRightData(newData)
	}
	/**
	 * 渲染左侧目录树
	 * contentEditable={true}会有光标闪现最前端的BUG，所以可编辑的div做成非受控组件（PS：递归渲染的div似乎很难解决此问题）
	 * input有换行bug，textarea有高度bug
	 * 经过取舍最后还是采用 contentEditable={true}
	 */
	const renderTree = tree => {
		if (_.isEmpty(tree)) {
			return
		}
		let level = 0;
		return _.map(tree, (o, idx) => {
			if (!_.isNil(o.level)) level = o.level;
			return <div className={`tree-box tree-item-${idx} level-${o.level}`} key={`${idx}-${o.level}`}
			            style={{marginLeft:  "30px"}}>
				{
					!_.isNil(o.level) && o.type !== "list" && <div className="tree-item-line" />
				}
				<div className="tree-item" style={{marginLeft: _.isNil(o.level) ? "10px" : ''}}>
					{
						((o.type === "image" || o.type === "paragraph" || o.type === "listItem") || o?.text) &&
							<div className="tree-item-position">
								<div className="tree-item-point"/>
								<div className="tree-item-box">
									<div className="tree-item-add">
										<span onClick={() => showOptions(o.id)}>+</span>
									</div>
									<div className={`tree-item-options ${o.showOptions ? 'active' : ''}`}>
										<ul>
											<li onClick={() => addItem(o, idx)}>添加节点</li>
											{
												 _.isNumber(o.level) && <li onClick={() => addChildItem(o, idx)}>添加子节点</li>
											}
											<li onClick={() => removeItem(o, idx)}>删除节点</li>
											<li>添加图片</li>
											<li>子节点添加图片</li>
										</ul>
									</div>
								</div>
							</div>

					}
					<div className="tree-item-content">
						{
							o.type === "image" && <img className="tree-item-img" src={o.src} alt=""/>
						}
						{
							o?.text && <div className="tree-item-content" contentEditable={true} suppressContentEditableWarning={true}
							                onInput={(e) => handleEditMd(e, idx, o.id)}>{o?.text}</div>
						}
					</div>
				</div>
				{
					renderTree(o.children)
				}
			</div>
		})
	}
	/**
	 * 输出新的markdown的 str
	 */
	const handleExport = () => {
		let newStr = toMarkdown(_.cloneDeep(rightData))
		alert(`输出markdown： \n${newStr}`)
	}
	

	return (
		<div className="md">

			<div className="md-left">
				{/*<div className="btn" onClick={handleExport}>输出新markdown</div>*/}
				<div className="btn two" onClick={exportPptx}>输出pptx</div>
				{renderTree(leftData)}
			</div>
			<div className="md-right">
				<WebPptx rightData={rightData}/>
			</div>
		</div>
	)
}

export default Home
