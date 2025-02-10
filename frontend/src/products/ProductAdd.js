import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import { toast } from 'react-toastify';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Product_Add = () => {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [category_uuid, setCategory_uuid] = useState('');
  const [quantity, setQuantity] = useState('');
  const [manufacturing_date, setManufacturing_date] = useState('');
  const [expiration_date, setExpiration_date] = useState('');
  const [avatar_uuid, setAvatar_uuid] = useState('');
  const [image, setImage] = useState(null);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Fonction pour récupérer les catégories
  const fetchCategories = async () => {
    const token = JSON.parse(localStorage.getItem('token'));
    const accessToken = token ? token.access_token : null;

    if (!accessToken) {
      toast.error('Veuillez vous connecter pour accéder à cette page');
      return;
    }

    try {
      const response = await axios.get('http://127.0.0.1:8000/api/v1/list', {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      setCategories(response.data);  // Mise à jour de l'état des catégories
    } catch (error) {
      toast.error("Erreur lors de la récupération des catégories.");
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  // Fonction pour gérer l'upload d'image
  const handleImageUpload = async (e) => {
    const formData = new FormData();
    formData.append('file', e.target.files[0]);

    const token = JSON.parse(localStorage.getItem('token'));
    const accessToken = token ? token.access_token : null;

    if (!accessToken) {
      toast.error('Veuillez vous connecter pour accéder à cette page');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/v1/storages/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${accessToken}`,
        },
      });
      setAvatar_uuid(response.data.uuid); // Récupère l'UUID de l'image
      toast.success("Image téléchargée avec succès.");
    } catch (error) {
      toast.error("Erreur lors du téléchargement de l'image.");
    }
  };

  // Fonction pour gérer la soumission du formulaire
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const token = JSON.parse(localStorage.getItem('token'));
    const accessToken = token ? token.access_token : null;
    if (!accessToken) {
      toast.error('Veuillez vous connecter pour accéder à cette page');
      return;
    }

    if (!name || !price || !category_uuid || !quantity || !manufacturing_date || !expiration_date || !avatar_uuid) {
      toast.error("Tous les champs doivent être remplis.");
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/v1/products', {
        name,
        price,
        category_uuid,
        quantity,
        manufacturing_date,
        expiration_date,
        avatar_uuid,
      }, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      toast.success("Produit ajouté avec succès.");
      navigate('/produits');
    } catch (error) {
      toast.error("Erreur lors de l'ajout du produit.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />
      <div className="container mt-4 py-5">
        <div className="card-box p-4 shadow-sm">
          <h4 className="text-brand mb-4 text-uppercase">Ajouter un Nouveau Produit</h4>
          <form onSubmit={handleSubmit}>
            <div className="row">
              <div className="col-md-6 mb-3">
                <label htmlFor="name" className="form-label">Nom du Produit</label>
                <input
                  type="text"
                  className="form-control form-control-lg shadow-none"
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>

              <div className="col-md-6 mb-3">
                <label htmlFor="price" className="form-label">Prix (FCFA)</label>
                <input
                  type="number"
                  className="form-control form-control-lg shadow-none"
                  id="price"
                  value={price}
                  onChange={(e) => setPrice(e.target.value)}
                />
              </div>
            </div>

            <div className="mb-3">
              <label htmlFor="category" className="form-label">Catégorie</label>
              <select
                id="category"
                className="form-select form-select-lg shadow-none"
                value={category_uuid}
                onChange={(e) => setCategory_uuid(e.target.value)}
              >
                <option value="">Sélectionnez une catégorie</option>
                {categories.map((category) => (
                  <option key={category.uuid} value={category.uuid}>
                    {category.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="row">
              <div className="col-md-6 mb-3">
                <label htmlFor="quantity" className="form-label">Quantité</label>
                <input
                  type="number"
                  className="form-control form-control-lg shadow-none"
                  id="quantity"
                  value={quantity}
                  onChange={(e) => setQuantity(e.target.value)}
                />
              </div>

              <div className="col-md-6 mb-3">
                <label htmlFor="manufacturing_date" className="form-label">Date de Fabrication</label>
                <input
                  type="date"
                  className="form-control form-control-lg shadow-none"
                  id="manufacturing_date"
                  value={manufacturing_date}
                  onChange={(e) => setManufacturing_date(e.target.value)}
                />
              </div>
            </div>

            <div className="row">
              <div className="col-md-6 mb-3">
                <label htmlFor="expiration_date" className="form-label">Date d'Expiration</label>
                <input
                  type="date"
                  className="form-control form-control-lg shadow-none"
                  id="expiration_date"
                  value={expiration_date}
                  onChange={(e) => setExpiration_date(e.target.value)}
                />
              </div>

              <div className="col-md-6 mb-3">
                <label htmlFor="image" className="form-label">Image du Produit</label>
                <input
                  type="file"
                  className="form-control form-control-lg shadow-none"
                  id="image"
                  onChange={handleImageUpload}
                />
              </div>
            </div>

            <div className="mb-3">
              <button
                type="submit"
                className="btn-primary"
                disabled={loading}
              >
                {loading ? 'En cours...' : 'Ajouter le Produit'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

export default Product_Add;
