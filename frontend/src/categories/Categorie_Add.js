import React, { useState } from 'react';
import Navbar from '../components/Navbar';  
import { toast } from 'react-toastify';  
import axios from 'axios';
import { useNavigate } from 'react-router-dom';  // Utilisation uniquement de useNavigate
const [loading, setLoading] = useState(false); 



const Categorie_Add = () =>{
    const navigate = useNavigate();
    const [name , setName] = useState('');
    const [description , setDescription] = useState('');
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false); 



    const handleSubmit = async (e) =>{
        e.preventDefault();
    }
    if(loading) return;
    if(!name){
        toast.error("Veuillez renseigner le nom de la catégorie");
        return;
    }
    const token = JSON.parse(localStorage.getItem('token'));
        const accessToken = token ? token.access_token : null;  // Extraire le access_token
        if (!accessToken) {
          toast.error('Veuillez vous connecter pour accéder à cette page');
          return;
    }
    const CategorieData = {name}

}