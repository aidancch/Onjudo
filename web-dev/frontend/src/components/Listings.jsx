import React, { useEffect, useState } from 'react';

function Listings() {
    const [listings, setListings] = useState([]);

    useEffect(() => {
        fetch("http://127.0.0.1:5000/api/listings")
            .then(response => response.json())
            .then(data => setListings(data));
    }, []);

    return (
        <div className="grid grid-cols-3 gap-4">
            {listings.map((listing, index) => (
                <div key={index} className="border p-4 rounded shadow-md bg-white">
                    <h3 className="text-lg font-bold">${listing.price.toLocaleString()}</h3>
                    <p className="text-gray-600">{listing.info}</p>
                    <p className="text-sm text-gray-400">{listing.address}</p>
                    <p className="mt-2">{listing.description}</p>
                </div>
            ))}
        </div>
    );
}

export default Listings;
