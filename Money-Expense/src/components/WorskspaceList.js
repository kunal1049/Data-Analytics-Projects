import React, { useState, useEffect, useRef } from "react";
import TutorialDataService from "../services/TutorialService";
import { makeStyles } from '@material-ui/core/styles';
import { CardActionArea, TableRow } from '@mui/material'
import {
    Grid,
    Card,
    CardContent,
    CardMedia,
    Typography,
    ButtonBase
} from '@material-ui/core/'

import img from "../images/1.jpg";
import { fontSize } from "@mui/system";

const useStyles = makeStyles(theme => ({
    root: {
        flexGrow: 1,
        padding: theme.spacing(2)
    }
}))

const mystyle = {
    color: "#4C445E",
    padding: "10px",
    fontFamily: "Roboto",
    fontSize:50
  };

const WorkspaceList = props => {

    const [workspace, setWorkspace] = useState([]);
    const workspaceRef = useRef(); 

    const classes = useStyles()

    workspaceRef.current = workspace;

    useEffect(() => {
        retrieveWorkspace();
    }, []);

    const retrieveWorkspace = () => {
        TutorialDataService.getAll()
          .then((response) => {          
            setWorkspace(response.data);              
          })
          .catch((e) => {
            console.log(e);
          });
      };

    const uniqueTags = [];
        workspace.map((item) => {     
        var findItem = uniqueTags.find((x) => x.workspace === item.workspace);
        if (!findItem) uniqueTags.push(item);
    });   

    const openWorkspace = (id) => {
        const workspace = workspaceRef.current[id].workspace;
    
        props.history.push("/workspace/" + workspace);
    };
    
   
    return(        
        <div className={classes.root}>
            <center style={mystyle}>Workspaces</center>
            <Grid
                container
                spacing={2}
                direction="row"
                justify="flex-start"
                alignItems="flex-start"
            >
                {uniqueTags.map(e => (                    
                    <Grid item xs={12} sm={6} md={3} key={workspace.indexOf(e)}>                    
                    <Card sx={{ maxWidth: 345 }} key={Card.id} onClick = {() => {openWorkspace(workspace.indexOf(e))}}>                       
                        <CardActionArea>                            
                            <CardMedia
                            component="img"
                            height="140"
                            image={img}
                            alt="green iguana"
                            />
                            <CardContent>
                            <Typography gutterBottom variant="h5" component="div">
                                {e.workspace}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                            
                            </Typography>
                            </CardContent>
                        </CardActionArea>                        
                    </Card>
                    
                    </Grid>
                ))}
            </Grid>
        </div>

    );
};

export default WorkspaceList;