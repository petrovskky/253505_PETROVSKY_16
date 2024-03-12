import React, { Component } from 'react'
import api from '../api'
import styled from 'styled-components'

const lightTheme = {
    primaryColor: '#212529',
    dangerColor: '#dc3545',
};

const Title = styled.h1.attrs({
    className: 'h2',
})`
    color: ${props => props.theme.primaryColor};
    margin: 5px 5px 0px;
`;

const Wrapper = styled.div.attrs({
    className: 'form-group',
})`
    margin: 0 auto;
    width: 600px;
`;

const Label = styled.label`
    margin: 5px;
    font-size: 1.2em;
    text-align: center;
`;

const InputText = styled.input.attrs({
    className: 'form-control',
})`
    margin: 5px;
    width: 100%;
    font-size: 1.2em;
    color: ${props => props.theme.primaryColor};
    background-color: ${props => props.theme.primaryColor};
    width: 100%;
`;

const Button = styled.button.attrs({
    className: `btn btn-primary`,
})`
    margin: 15px 15px 15px 5px;
    background-color: ${props => props.theme.primaryColor};
    padding: 10px 20px;
    font-size: 1.2em;
    width: 100%;
`;

const CancelButton = styled.a.attrs({
    className: `btn btn-danger`,
})`
    margin: 15px 15px 15px 5px;
    background-color: ${props => props.theme.dangerColor};
    padding: 10px 20px;
    font-size: 1.2em;
    width: 100%;
`;

const ButtonContainer = styled.div`
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
    margin-left: 20px;
`;

class MoviesInsert extends Component {
    constructor(props) {
        super(props);

        this.state = {
        name: '',
        rating: '',
        time: '',
        };
    }

    handleChangeInputName = async event => {
        const name = event.target.value;
        this.setState({ name });
    };

    handleChangeInputRating = async event => {
        const rating = event.target.validity.valid
        ? event.target.value
        : this.state.rating;

        this.setState({ rating });
    };

    handleChangeInputTime = async event => {
        const time = event.target.value;
        this.setState({ time });
    };

    handleIncludeMovie = async () => {
        const { name, rating, time } = this.state;
        const arrayTime = time.split('/');
        const payload = { name, rating, time: arrayTime };

        await api.insertMovie(payload).then(res => {
            window.alert(`Movie inserted successfully`);
            this.setState({
                name: '',
                rating: '',
                time: '',
        });
        });
    };

    render() {
        const { name, rating, time } = this.state
        return (
            <Wrapper>
                <Title theme={lightTheme}>Create Movie</Title>

                <Label>Name:</Label>
                <InputText
                    type="text"
                    value={name}
                    onChange={this.handleChangeInputName}
                />

                <Label>Rating:</Label>
                <InputText
                    type="number"
                    step="0.1"
                    lang="en-US"
                    min="0"
                    max="10"
                    pattern="[0-9]+([,\.][0-9]+)?"
                    value={rating}
                    onChange={this.handleChangeInputRating}
                />

                <Label>Time:</Label>
                <InputText
                    type="text"
                    value={time}
                    onChange={this.handleChangeInputTime}
                />

                <ButtonContainer>
                    <Button onClick={this.handleIncludeMovie}>
                        Add Movie
                    </Button>
                    <CancelButton href={'/movies/list'}>
                        Cancel
                    </CancelButton>
                </ButtonContainer>
            </Wrapper>
        )
    }
}

export default MoviesInsert