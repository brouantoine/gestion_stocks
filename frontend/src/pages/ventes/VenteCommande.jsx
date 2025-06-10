import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ClientSelector from './ClientSelector';
import TypeSelector from './TypeSelector';
import ProductAdder from './ProductAdder';
import ProductList from './ProductList';
import SubmitButton from '../../components/button/SubmitButton';
import '../../css/VenteCommande.css'
const VenteCommande = () => {
  const [typeTransaction, setTypeTransaction] = useState('VENTE_DIRECTE');
  const [client, setClient] = useState(null);
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [discount, setDiscount] = useState(0);
  const [defaultClient, setDefaultClient] = useState(null);
  const [tva, setTva] = useState(1);
  useEffect(() => {
    const fetchDefaultClient = async () => {
      try {
        const response = await axios.get('/api/clients/', {
          params: { search: 'Client Direct' }
        });
        if (response.data.length > 0) {
          setDefaultClient(response.data[0]);
          if (typeTransaction === 'VENTE_DIRECTE') {
            setClient(response.data[0]);
          }
        }
      } catch (error) {
        console.error("Erreur lors du chargement du client par défaut:", error);
      }
    };
    fetchDefaultClient();
  }, []);

  const handleTransactionTypeChange = (type) => {
    setTypeTransaction(type);
    if (type === 'VENTE_DIRECTE' && defaultClient) {
      setClient(defaultClient);
    } else {
      setClient(null);
    }
  };

  const handleAddProduct = () => {
    if (!selectedProduct) return;
    
    const newItem = {
      product: selectedProduct,
      quantity,
      unitPrice: selectedProduct.prix_vente,
      discount
    };

    setProducts([...products, newItem]);
    resetProductForm();
  };

  const resetProductForm = () => {
    setSelectedProduct(null);
    setQuantity(1);
    setDiscount(0);
  };

  const handleRemoveProduct = (index) => {
    setProducts(products.filter((_, i) => i !== index));
  };

  const handleSubmit = async () => {
    try {
      if ((!client || products.length === 0) && typeTransaction !== 'VENTE_DIRECTE') {
        alert("Veuillez sélectionner un client et ajouter des produits");
        return;
      }

      const payload = {
        client: typeTransaction === 'VENTE_DIRECTE' ? defaultClient.id : client.id,
        is_vente_directe: typeTransaction === 'VENTE_DIRECTE',
        statut: typeTransaction === 'VENTE_DIRECTE' ? 'VALIDEE' : 'BROUILLON',
        tva: tva, 
        lignes: products.map(product => ({
          produit: product.product.id,
          quantite: parseInt(product.quantity, 10),
          prix_unitaire: parseFloat(product.unitPrice),
          remise_ligne: parseFloat(product.discount) || 0
        }))
      };

      const response = await axios.post(
        'http://localhost:8000/api/commandes-client/', 
        payload,
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        }
      );

      if (response.status === 201) {
        alert("Transaction enregistrée avec succès!");
        setClient(typeTransaction === 'VENTE_DIRECTE' ? defaultClient : null);
        setProducts([]);
      }
    } catch (error) {
      console.error("Erreur détaillée:", error.response?.data || error.message);
      alert("Erreur lors de l'enregistrement. Voir la console pour plus de détails.");
    }
  };

  return (
    <div className="vente-container">
      <h2 className="vente-title">{typeTransaction === 'VENTE_DIRECTE' ? 'Vente Directe' : 'Commande Client'}</h2>
      
      <div className="form-section">
        <h3 className="section-title">Type de Transaction</h3>
        <TypeSelector 
          transactionType={typeTransaction}
          setTransactionType={handleTransactionTypeChange}
        />
      </div>

      <div className="form-section">
        <h3 className="section-title">Informations Client</h3>
        <ClientSelector 
          selectedClient={client}
          setSelectedClient={setClient}
          isDirectSale={typeTransaction === 'VENTE_DIRECTE'}
        />
      </div>

      <div className="form-section">
        <h3 className="section-title">Paramètres Financiers</h3>
        <div className="tva-selector">
          <label>TVA Applicable</label>
          <select 
            value={tva}
            onChange={(e) => setTva(e.target.value)}
            className="form-control"
          >
            <option value={1}>18% (TVA standard)</option>
            <option value={2}>10% (TVA réduite)</option>
            <option value={3}>5.5% (TVA spéciale)</option>
          </select>
        </div>
      </div>

      <div className="form-section">
        <h3 className="section-title">Ajout de Produits</h3>
        <ProductAdder
          selectedProduct={selectedProduct}
          setSelectedProduct={setSelectedProduct}
          quantity={quantity}
          setQuantity={setQuantity}
          discount={discount}
          setDiscount={setDiscount}
          onAdd={handleAddProduct}
        />
      </div>

      <div className="form-section">
        <ProductList 
          products={products}
          onRemove={handleRemoveProduct}
        />
      </div>

      <SubmitButton
        transactionType={typeTransaction}
        disabled={(!client && typeTransaction !== 'VENTE_DIRECTE') || products.length === 0}
        onSubmit={handleSubmit}
      />
    </div>
  );
};

export default VenteCommande;