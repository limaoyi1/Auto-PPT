/**
 * description： 在线渲染pptx组件
 * @author Kevin
 * @date 2023/8/17
 */
import "./index.scss"
// Import Swiper React components
import {Swiper, SwiperSlide} from 'swiper/react';
import {Navigation, Pagination} from "swiper";
// Import Swiper styles
import "swiper/css/navigation";
// Import Swiper styles
import 'swiper/css';
import {useEffect, useState} from "react";
import utils from "@utils";
import _ from "lodash";

let list = [];

function WebPptx(props) {
	let list = [];
	const {rightData} = props
	
	useEffect(() => {
		renderAllSlide()
	}, [])
	/**
	 * 展平树结构 -> pptx所需数组
	 * @param data
	 */
	const flattenTree = data =>{
		_.map(data, o=>{
			if(o.type==="section"){
				list.push(o)
				flattenTree(o?.children)
			}
		})
		return list
	}
	/**
	 * 绘制全部幻灯片
	 */
	const renderAllSlide = () => {
		let pptxData = flattenTree(rightData)
		console.log(pptxData, '=======pptxData=======')
		return (
			<>
				<SwiperSlide>
					<div className="cover-slide" style={{textAlign: "center", fontSize: 24, fontWeight: 'bold'}}>
						{_.get(pptxData, `0.text`)}
					</div>
				</SwiperSlide>
				{
					_.map(pptxData, (o, idx)=>{
						return (
							<div key={idx}>
								<SwiperSlide >
									<div className="common-slide">
										<div className="common">
											<h2>{o?.text}</h2>
											<div>
												{_.map(_.get(o, `children`), p => {
													let hasImg = _.findIndex(_.get(o, `children`), a=> a.type === "image") > -1;
													let textCount = _.size(p?.text);
													if(p?.type === "list"){
														_.map(p?.children, a=>{
															textCount += _.size(a?.text)
														})
													}
													return (
														<>
															{
																p?.text && <div className="common-content" key={p?.id}
																  style={{fontSize: textCount > 160 ? "8px" : textCount > 120 ? "10px" : "16px",
																	  width: hasImg ? "60%" : "100%"}}>
																	{p?.text}
																</div>
															}
															{
																p?.type === "list" &&
																<ul className="common-list">
																	{
																		_.map(p?.children, q=>{
																			return <li key={q?.id}>{q?.text}</li>
																		})
																	}
																</ul>
															}
															{
																p?.type === "image" && <img className="common-img" src={p?.src} alt=""/>
															}
														</>
													)
												})}
											</div>
										</div>
									</div>
								</SwiperSlide>
							</div>
						)
					})
				}
			</>
		)
	}

	return (
		<div className="web-pptx">
			<Swiper
				className="swiper"
				navigation={true}
				pagination={{
					type: 'fraction',
				}}
				modules={[Navigation, Pagination]}
				onSlideChange={() => console.log('slide change')}
				onSwiper={(swiper) => console.log(swiper)}
			>
				{renderAllSlide()}
			</Swiper>
		</div>
	)
}

export default WebPptx;
