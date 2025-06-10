import React, { useEffect, useState } from 'react';

const ClientSelector = ({ selectedClient, setSelectedClient, isDirectSale }) => {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/clients/')
      .then(res => res.json())
      .then(data => {
        setClients(data);
        setLoading(false);
      });
  }, []);

  return (
    <div className="client-selector">
      <h3>Client</h3>
      {loading ? (
        <p>Chargement des clients...</p>
      ) : (
        <select
          value={selectedClient?.id || ''}
          onChange={(e) => {
            const selected = clients.find(c => c.id === parseInt(e.target.value));
            setSelectedClient(selected || null);
          }}
          disabled={isDirectSale}
        >
          <option value="">{isDirectSale ? "Client Direct (par défaut)" : "Sélectionnez un client"}</option>
          {clients.map(client => (
            <option key={client.id} value={client.id}>
              {client.nom_client}
            </option>
          ))}
        </select>
      )}
    </div>
  );
};

export default ClientSelector;