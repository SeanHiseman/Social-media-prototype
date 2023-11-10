import React, { createContext, useContext, useState, useEffect } from 'react';

const UserContext = createContext(null);

export const useUser = () => useContext(UserContext);

export const UserProvider = ({ children }) => {
    const [user, setUser ] = useState(null);
    useEffect(() => {
        fetch('/api/get_current_user')
            .then(response => response.json())
            .then(data => {
                if (data.user_id) {
                    setUser({ id: data.user_id});
                }
            })
    }, []);

    return (
        <UserContext.Provider value={{ user, setUser }}>
            {children}
        </UserContext.Provider>
    );
};