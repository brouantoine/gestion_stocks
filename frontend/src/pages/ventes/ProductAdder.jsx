import React, { useEffect, useState } from 'react';
import '../../css/VenteCommande.css'

const ProductAdder = ({
  selectedProduct,
  setSelectedProduct,
  quantity,
  setQuantity,
  discount,
  setDiscount,
  onAdd
}) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/produits/')
      .then(res => res.json())
      .then(data => {
        setProducts(data);
        setLoading(false);
      });
  }, []);

    return (
    <div className="product-adder">
      {loading ? (
        <p>Chargement des produits...</p>
      ) : (
        <div className="product-form">
          <div className="form-group">
            <label>Produit</label>
            <select
              value={selectedProduct?.id || ''}
              onChange={(e) => {
                const selected = products.find(p => p.id === parseInt(e.target.value));
                setSelectedProduct(selected || null);
              }}
              className="form-control"
            >
              <option value="">Sélectionnez un produit</option>
              {products.map(product => (
                <option key={product.id} value={product.id}>
                  {product.designation} - {product.prix_vente}€
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label>Quantité</label>
            <input
              type="number"
              value={quantity}
              onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
              min="1"
              className="form-control"
            />
          </div>
          
          <div className="form-group">
            <label>Remise (%)</label>
            <input
              type="number"
              value={discount}
              onChange={(e) => setDiscount(parseFloat(e.target.value) || 0)}
              min="0"
              max="100"
              step="0.5"
              className="form-control"
            />
          </div>
          
          <button 
            onClick={onAdd}
            className="add-button"
            disabled={!selectedProduct}
          >
            Ajouter au panier
          </button>
        </div>
      )}
    </div>
  );
};

export default ProductAdder;