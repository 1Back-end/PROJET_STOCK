import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { toast } from 'react-toastify';
import Navbar from '../components/Navbar';
const ProductDetails = () => {
  const { uuid } = useParams(); // Récupère l'UUID du produit depuis l'URL
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProductDetails = async () => {
      const token = JSON.parse(localStorage.getItem('token'));
      const accessToken = token ? token.access_token : null;

      if (!accessToken) {
        toast.error("Vous devez être connecté pour afficher les détails.");
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/v1/products/${uuid}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (response.data) {
          setProduct(response.data);
        } else {
          toast.error("Produit introuvable.");
        }
      } catch (error) {
        toast.error("Erreur lors du chargement du produit.");
      } finally {
        setLoading(false);
      }
    };

    fetchProductDetails();
  }, [uuid]);

  if (loading) {
    return <p>Chargement...</p>;
  }

  if (!product) {
    return <p>Produit introuvable.</p>;
  }

  return (
    <>
      <Navbar />
    <div className="container mt-5 py-5">
      <div className="card-box shadow-sm border-0 p-4">
        <h3 className="text-brand">{product.name}</h3>
        <div className="row">
          <div className="col-md-6">
            <img 
              src={product.avatar ? product.avatar.url : 'https://via.placeholder.com/300'} 
              alt={product.name} 
              className="img-fluid rounded"
            />
          </div>
          <div className="col-md-6">
            <p className='mb-3'><strong>Catégorie :</strong> {product.category ? product.category.name : 'Inconnue'}</p>
            <p className='mb-3'><strong>Quantité :</strong> {product.quantity}</p>
            <p className='mb-3'><strong>Prix :</strong> {product.price} FCFA</p>
            <p className='mb-3'><strong>Date de fabrication :</strong> {new Date(product.manufacturing_date).toLocaleDateString()}</p>
            <p className='mb-3'><strong>Date d'expiration :</strong> {new Date(product.expiration_date).toLocaleDateString()}</p>
            <p className='mb-3'><strong>Ajouté le :</strong> {new Date(product.created_at).toLocaleString()}</p>
            <p className='mb-3'><strong>Mis à jour le :</strong> {new Date(product.updated_at).toLocaleString()}</p>
            <p className='mb-3'><strong>Créé par :</strong> {product.created_by.first_name} {product.created_by.last_name} ({product.created_by.role})</p>
          </div>
        </div>
      </div>
    </div>
    </>
  );
};

export default ProductDetails;
