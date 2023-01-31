import React, { useState, useEffect, useMemo, useRef } from "react";
import TutorialDataService from "../services/TutorialService";
import TutorialsList from "./TutorialsList";
import { useTable } from "react-table";
import { ToWords } from 'to-words';
import ReactHTMLTableToExcel from 'react-html-table-to-excel';

const Workspace = (props) => {

  const [currentWorkspace, setcurrentWorkspace] = useState([]);
  const [searchTitle, setSearchTitle] = useState("");
  var total = 0;

  const toWords = new ToWords({
    localeCode: 'en-IN',
    converterOptions: {
      currency: true,
      ignoreDecimal: false,
      ignoreZeroCurrency: false,
      doNotAddOnly: false,
    }
  });
      
  const getWorkspace = workspace => {
    TutorialDataService.getWorkspace(workspace)
      .then(response => {
      setcurrentWorkspace(response.data);
      //console.log(response.data.description);
    })
    .catch(e => {
      console.log(e);
    });
  };

  console.log(currentWorkspace);

  //console.log(props.match.params.workspace);

  useEffect(() => {                
    getWorkspace(props.match.params.workspace);
  }, [props.match.params.workspace]);

  const onChangeSearchTitle = (e) => {
    const searchTitle = e.target.value;
    setSearchTitle(searchTitle);
  }

  const refreshList = () => {
    TutorialsList.retrieveTutorials();
  };

  const removeAllTutorials = () => {
    TutorialDataService.removeAll()
      .then((response) => {
        console.log(response.data);
        refreshList();
      })
      .catch((e) => {
        console.log(e);
      });
  };

  const findByTitle = () => {
    TutorialDataService.findByTitle(searchTitle)
      .then((response) => {
        setcurrentWorkspace(response.data);        
      })
      .catch((e) => {
        console.log(e);
      });
  };

  const columns = useMemo(
    () => [
      {
        Header: "Title",
        accessor: "title",
      },
      {
        Header: "Description",
        accessor: "description",
      },
      {
        Header: "Workspace",
        accessor: "workspace",        
      },      
    ],
    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({
    columns,
    data: currentWorkspace,
  });


  currentWorkspace.map((item) => {        
      total = parseInt(item.description) + total;
  });  

  console.log(total);

  return(
    <div className="list row">

    <div className="col-md-8">
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Search by title"
          value={searchTitle}
          onChange={onChangeSearchTitle}
        />
        <div className="input-group-append">
          <button
            className="btn btn-outline-secondary"
            type="button"
            onClick={findByTitle}
          >
            Search
          </button>
        </div>
      </div>
    </div>
    <div className="col-md-12 list">
      <table
        className="table table-striped table-bordered"
        {...getTableProps()}
        id="table-export"
      >
        <thead>
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <th {...column.getHeaderProps()}>
                  {column.render("Header")}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map((row, i) => {
            prepareRow(row);             
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map((cell) => {
                  return (
                    <td {...cell.getCellProps()}>{cell.render("Cell")}</td>                      
                  );
                })}
              </tr>
            );
          })}
        </tbody>
      </table>
      
    </div>

    <div className="col-md-8">

      <div className="mb-3">          
        Total  : {total} ({toWords.convert(total)})
      </div>

      <div className="mb-3">
        <ReactHTMLTableToExcel
          id="test-table-xls-button"
          className="download-table-xls-button"
          table="table-export"
          filename="expense"
          sheet="tablexls"
          buttonText="Download as XLS"/>            
      </div>        
     
    </div>
  

    <div className="col-md-8">
      <button className="btn btn-sm btn-danger" onClick={removeAllTutorials}>
        Remove All
      </button>
    </div>
  </div>
  
  );
    
};

export default Workspace;


