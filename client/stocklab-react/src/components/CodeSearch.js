import React, { Component } from 'react';
import Select from 'react-select';
// import makeAnimated from 'react-select/lib/animated';
import RadioGroup from '@material-ui/core/RadioGroup';
import Radio from '@material-ui/core/Radio';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';

class CodeSearch extends Component {
    constructor(props) {
        super(props);
        console.log("CodeSearch constructor")
        this.state = {
            selectedOption: '',
            options: [],
            filteredOptions: [],
        };
    }
    handleSelectChange = (selectedOption) => {
        this.props.handleSelectCode(selectedOption.code);
    }
    handleRadioChange = (event) => {
        if(event.target.value === "spac") {
            this.setState({
                filteredOptions: this.state.options.filter(item=>item.is_spac === 'Y')
            })
        }else if(event.target.value === 'etf') {
            this.setState({
                filteredOptions: this.state.options.filter(item => item.is_etf === '1')
            })
        }else if(event.target.value === 'all') {
            this.setState({
                filteredOptions: [],
            })
        }
    }
    componentDidMount() {
        console.log("CodeSearch didmount");
        let api_url = "http://127.0.0.1:5000/codes";
        let options = [];
        fetch(api_url)
            .then(res => res.json())
            .then(data => { 
                console.log('/codes =>',data);
                data["result"].map(function(item) {
                    item["value"] = item["code"]
                    item["label"] = item["name"] + "(" + item["code"] + ")"
                    item["market"] = item["market"]
                    item["is_etf"] = item["is_etf"]
                    item["is_spac"] = item["is_spac"]
                });
                this.setState({options:data["result"]})
            });
    }
    render() {
        const { selectedOption, options, filteredOptions } = this.state;
        console.log("CodeSearch render", options);
        return (
            <div>
                {
                    <Select
                        onChange = {this.handleSelectChange}
                        options = {filteredOptions.length > 0 ? filteredOptions : options}
                    />
                }
                {
                    <FormControl component = "fieldset">
                        <RadioGroup
                            onChange={this.handleRadioChange}
                            row
                            >
                            <FormControlLabel
                                value="all"
                                control={<Radio color="primary"/>}
                                label="ALL"
                                labelPlacement="end"
                            />
                            <FormControlLabel
                                value="etf"
                                control={<Radio color="primary"/>}
                                label="ETF"
                                labelPlacement="end"
                            />
                            <FormControlLabel
                                value="spac"
                                control={<Radio color="primary"/>}
                                label="SPAC"
                                labelPlacement="end"
                            />
                        </RadioGroup>
                    </FormControl>
                }
            </div>
        )
    }
}

export default CodeSearch;