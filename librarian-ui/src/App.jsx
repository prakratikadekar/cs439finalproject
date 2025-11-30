import { useState } from "react";
import Home from "./home.jsx";
import Recommend from './recommendation.jsx';

function App() {
    const [currentPage, SetCurrentPage] = useState('home');
    const [userRecommendations, setUserRecommendation] = useState(null);
    const [userQuery, setUserQuery] = useState('');

    const ToRecommendationPage = (data, searchQuery) => {
        setUserRecommendation(data);
        setUserQuery(searchQuery)
        SetCurrentPage('recommendation')
    };

    const ToHomePage = () => {
        setUserRecommendation(null);
        setUserQuery('')
        SetCurrentPage('home')
    };
 

    
    return (
        <div>
            {currentPage === 'home' && (
                <Home ToRecommendationPage = {ToRecommendationPage} />
            )}

            {currentPage === 'recommendation' && (
                <Recommend recommendations = {userRecommendations} query = {userQuery} ToHomePage = {ToHomePage} />
            )}
        </div>
    );
}

export default App;
