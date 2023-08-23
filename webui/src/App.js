import "./App.scss"
import { HashRouter, Route, Routes } from "react-router-dom"
import Home from "@/pages/home"

function App() {

	return (
		<div className="App">
			<HashRouter path="/*">
				<Routes>
					<Route path="/" element={<Home />} />
				</Routes>
			</HashRouter>
		</div>
	)
}

export default App
