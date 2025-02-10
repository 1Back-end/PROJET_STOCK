import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import { toast } from 'react-toastify';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';

const Product_Edit = () => {
  const { uuid } = useParams();
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [category_uuid, setCategory_uuid] = useState('');
  const [quantity, setQuantity] = useState('');
  const [manufacturing_date, setManufacturing_date] = useState('');
  const [expiration_date, setExpiration_date] = useState('');
  const [avatar_uuid, setAvatar_uuid] = useState('');
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const getAccessToken = () => {
    const token = JSON.parse(localStorage.getItem('token'));
    return token ? token.access_token : null;
  };

  const fetchCategories = async () => {
    const accessToken = getAccessToken();
    if (!accessToken) {
      toast.error('Veuillez vous connecter');
      return;
    }
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/v1/list', {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      setCategories(response.data);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erreur lors de la récupération des catégories');
    }
  };

  const fetchProduct = async () => {
    const accessToken = getAccessToken();
    if (!accessToken) {
      toast.error('Veuillez vous connecter');
      return;
    }
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/v1/products/${uuid}`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      const product = response.data;
      setName(product.name);
      setPrice(product.price);
      setCategory_uuid(product.category_uuid);
      setQuantity(product.quantity);
      setManufacturing_date(product.manufacturing_date);
      setExpiration_date(product.expiration_date);
      setAvatar_uuid(product.avatar_uuid);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erreur lors de la récupération du produit');
    }
  };

  useEffect(() => {
    fetchCategories();
    fetchProduct();
  }, [uuid]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const accessToken = getAccessToken();
    if (!accessToken) {
      toast.error('Veuillez vous connecter');
      return;
    }

    const data = {
      uuid,
      name: name || null,
      price: price ? parseFloat(price) : null,
      category_uuid: category_uuid || null,
      quantity: quantity ? parseInt(quantity, 10) : null,
      manufacturing_date: manufacturing_date || null,
      expiration_date: expiration_date || null,
      avatar_uuid: avatar_uuid || null,
    };

    try {
      await axios.put("http://127.0.0.1:8000/api/v1/products", data, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      toast.success("Produit modifié avec succès");
      navigate('/produits');
    } catch (error) {
      toast.error(error.response?.data?.detail || "Erreur lors de la modification du produit");
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return; // Image non obligatoire, ne rien faire si aucun fichier n'est sélectionné

    const formData = new FormData();
    formData.append('file', file);

    const accessToken = getAccessToken();
    if (!accessToken) {
      toast.error('Veuillez vous connecter');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/v1/storages/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${accessToken}`,
        },
      });
      setAvatar_uuid(response.data.uuid);
      toast.success("Image téléchargée avec succès.");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Erreur lors du téléchargement de l'image.");
    }
  };

  return (
    <>
      <Navbar />
      <div className="container mt-4 py-5">
        <div className="card-box p-4 shadow-sm">
          <h4 className="text-brand mb-4 text-uppercase">Modifier le Produit</h4>
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="form-label">Nom du Produit</label>
              <input type="text" className="form-control form-control-lg shadow-none" value={name} onChange={(e) => setName(e.target.value)} />
            </div>
            <div className="mb-3">
              <label className="form-label">Prix (FCFA)</label>
              <input type="number" className="form-control form-control-lg shadow-none" value={price} onChange={(e) => setPrice(e.target.value)} />
            </div>
            <div className="mb-3">
              <label className="form-label">Catégorie</label>
              <select className="form-select form-select-lg shadow-none select-custom" value={category_uuid} onChange={(e) => setCategory_uuid(e.target.value)}>
                <option>Sélectionnez une catégorie</option>
                {categories.map((category) => (
                  <option key={category.uuid} value={category.uuid}>{category.name}</option>
                ))}
              </select>
            </div>
            <div className="mb-3">
              <label className="form-label">Quantité</label>
              <input type="number" className="form-control form-control-lg shadow-none" value={quantity} onChange={(e) => setQuantity(e.target.value)} />
            </div>
            <div className="mb-3">
              <label className="form-label">Date de Fabrication</label>
              <input type="date" className="form-control form-control-lg shadow-none" value={manufacturing_date} onChange={(e) => setManufacturing_date(e.target.value)} />
            </div>
            <div className="mb-3">
              <label className="form-label">Date d'Expiration</label>
              <input type="date" className="form-control form-control-lg shadow-none" value={expiration_date} onChange={(e) => setExpiration_date(e.target.value)} />
            </div>
            <div className="mb-3">
              <label className="form-label">Image du Produit</label>
              <input type="file" className="form-control" onChange={handleImageUpload} />
            </div>
            <div className="mb-3">
              <button type="submit" className="btn btn-primary" disabled={loading}>{loading ? 'En cours...' : 'Modifier le Produit'}</button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

export default Product_Edit;
