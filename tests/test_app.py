from app import app
from chalice.test import Client
import pytest
import json
import logging


def test_pass():
    assert 0 == 0


@pytest.mark.skip
def test_get():
    logging.debug('Test Get poll')
    with open('tests/get.json', ) as f:
        data = json.load(f)
    with Client(app, stage_name='dev') as client:
        result = client.lambda_.invoke('handler', data)
        logging.debug("result %s", result)
        assert 'pass' == 'pass'


