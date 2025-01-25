import React from 'react';
import Chat from './components/Chat';
import Listings from './components/Listings';

function App() {
    return (
        <div className="flex h-screen">
            {/* Left: Listings */}
            <div className="w-2/3 p-4 bg-gray-100">
                <Listings />
            </div>
            {/* Right: Chat */}
            <div className="w-1/3 p-4 bg-white border-l">
                <Chat />
            </div>
        </div>
    );
}

export default App;
