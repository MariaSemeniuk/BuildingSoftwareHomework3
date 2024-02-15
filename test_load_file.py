def test_load_file():
    from load_file import load_file

    #get the question
    file = "/Users/mariasemeniuk/Documents/GitHub/UofT-DSI/python/vehicles-utilizing-green-technology-november-2023.xlsx"
    df = load_file(file)

    #get the answer
    shape = (1037, 8)

    # assert they are the same
    assert df.shape == shape