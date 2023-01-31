import React from "react";
import { Switch, Route, Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "@fortawesome/fontawesome-free/css/all.css";
import "@fortawesome/fontawesome-free/js/all.js";
import "./App.css";

import Avatar from '@mui/material/Avatar';
import { makeStyles } from '@material-ui/core/styles'

import AddTutorial from "./components/AddTutorial";
import Tutorial from "./components/Tutorial";
import TutorialsList from "./components/TutorialsList";
import WorkspaceList from "./components/WorskspaceList";
import Workspace from "./components/Workspace";
import img from "./images/2.jpg";

const useStyles = makeStyles(theme => ({   
  alignItemsAndJustifyContent: {      
    display:"flex" ,
    alignItems:"right",
    justifyContent:"right",
  }
}))

function App() {
  const classes = useStyles()
  return (
    <div>
      <nav className="navbar navbar-expand navbar-dark bg-dark ml-auto">
        <Link to="/" className="nav-link">
          Devansh Expense
        </Link>
        <div className="navbar-nav mr-auto">
          <li className="nav-item">
            <Link to={"/workspace"} className="nav-link">
              Expense
            </Link>
          </li>
          <li className="nav-item">
            <Link to={"/add"} className="nav-link">
              Add
            </Link>
          </li>                           
        </div>
        <div className="navbar-nav ml-auto">
          <li className="nav-item">
            <Avatar src={img} />
          </li>
        </div>        
      </nav>      

      <div className="container mt-3">
        <Switch>
        <Route exact path={["/", "/tutorials"]} component={TutorialsList} />
          <Route exact path="/workspace" component={WorkspaceList} />
          <Route exact path="/add" component={AddTutorial} />
          <Route path="/tutorials/:id" component={Tutorial} />
          <Route path="/workspace/:workspace" component={Workspace} />

        </Switch>
      </div>
    </div>
  );
}

export default App;
