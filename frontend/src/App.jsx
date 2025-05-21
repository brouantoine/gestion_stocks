// import React from 'react';
// import { Routes, Route } from 'react-router-dom';
// import ProduitList from './pages/Produits/ProduitList';
// import CommandeList from './pages/commandes/CommandeList';
// import NavBar from './components/NavBar';

// function App() {
//   return (
//     <div className="App">s
//       <NavBar>
//         <Routes>
//           <Route path="/" element={<ProduitList />} />
//           <Route path="/produits" element={<ProduitList />} />
//           <Route path="/commandes" element={<CommandeList />} />
//         </Routes>
//       </NavBar>
//     </div>
//   );
// }

// export default App;


// import React from 'react';
// import { Routes, Route } from 'react-router-dom';
// import NavBar from './components/NavBar';
// import ProduitList from './pages/Produits/ProduitList';
// import CommandeList from './pages/commandes/CommandeList';
// import { Layout } from 'antd';

// const { Content } = Layout;

// function App() {
//   return (
//     <NavBar>
//       <Layout style={{ marginLeft: 200, minHeight: '100vh' }}>
//         <Content style={{ margin: '24px 16px', padding: 24 }}>
//           <Routes>
//             <Route path="/" element={<ProduitList />} />
//             <Route path="/produits" element={<ProduitList />} />
//             <Route path="/commandes" element={<CommandeList />} />
//           </Routes>
//         </Content>
//       </Layout>
//     </NavBar>
//   );
// }

// export default App;


import React from 'react';
import { Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import ProduitList from './pages/Produits/ProduitList';
import CommandeList from './pages/commandes/CommandeList';
import NouvelleCommande from './pages/commandes/NouvelleCommande'; 
import DetailCommande from './pages/commandes/DetailCommande'; 
import Dashboard from './pages/Dashboard/Dashboard';
import ClientList from './pages/Clients/ClientList';
import ClientDetail from './pages/Clients/ClientDetail';
import Login from './pages/auth/Login'
function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="*" element={
        <NavBar>
          <Routes>
            <Route path='/login' element={<Login />}/>
            <Route path="/produits" element={<ProduitList />} />
            <Route path="/commandes" element={<CommandeList />} />
            <Route path="/commandes/nouveau" element={<NouvelleCommande />} />
            <Route path="/commandes/:id" element={<DetailCommande />} />
            <Route path="/clients" element={<ClientList />} />
            <Route path="/clients/:id" element={<ClientDetail />} />
          </Routes>
        </NavBar>
      } />
    </Routes>
  );
}
export default App;