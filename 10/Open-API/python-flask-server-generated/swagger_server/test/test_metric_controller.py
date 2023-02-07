# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.metric import Metric  # noqa: E501
from swagger_server.test import BaseTestCase


class TestMetricController(BaseTestCase):
    """MetricController integration test stubs"""

    def test_add_metric(self):
        """Test case for add_metric

        Add a new metric to the DB
        """
        body = Metric()
        data = dict(id=789,
                    cpu_model='cpu_model_example',
                    cpu_cores=789,
                    ram_capacity='ram_capacity_example')
        response = self.client.open(
            '/api/metric',
            method='POST',
            data=json.dumps(body),
            data=data,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_metric(self):
        """Test case for delete_metric

        Deletes a Metric
        """
        response = self.client.open(
            '/api/metric/{metricId}'.format(metric_id=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_metrics(self):
        """Test case for get_all_metrics

        Get all metrics
        """
        response = self.client.open(
            '/api/metric',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_metric_by_id(self):
        """Test case for get_metric_by_id

        Find metric by ID
        """
        response = self.client.open(
            '/api/metric/{metricId}'.format(metric_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_metric(self):
        """Test case for update_metric

        Update an existing metric
        """
        body = Metric()
        data = dict(id=789,
                    cpu_model='cpu_model_example',
                    cpu_cores=789,
                    ram_capacity='ram_capacity_example')
        response = self.client.open(
            '/api/metric',
            method='PUT',
            data=json.dumps(body),
            data=data,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_metric_with_form(self):
        """Test case for update_metric_with_form

        Updates a metric in the DB with form data
        """
        query_string = [('cpu_model', 'cpu_model_example'),
                        ('cpu_cores', 789),
                        ('ram_capacity', 'ram_capacity_example')]
        response = self.client.open(
            '/api/metric/{metricId}'.format(metric_id=789),
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
