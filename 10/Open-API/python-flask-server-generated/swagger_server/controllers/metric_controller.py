import connexion
import six

from swagger_server.models.metric import Metric  # noqa: E501
from swagger_server import util

metrics = [
    {"id": 1,
     "cpu_model": "Intel",
     "cpu_cores": 4,
     "ram_capacity": "4 GB"
     }
]


def add_metric(body):  # noqa: E501
    """Add a new metric to the DB

    Add a new metric to the DB # noqa: E501

    :param body: Create a new metric in the DB
    :type body: dict | bytes

    :rtype: Metric
    """
    global metrics
    if connexion.request.is_json:
        body = Metric.from_dict(connexion.request.get_json())  # noqa: E501
    payload = {
        "id": body.id,
        "cpu_model": body.cpu_model,
        "cpu_cores": body.cpu_cores,
        "ram_capacity": body.ram_capacity
    }

    metrics.append(payload)
    return payload


# def add_metric(id, cpu_model, cpu_cores, ram_capacity):  # noqa: E501
#     """Add a new metric to the DB

#     Add a new metric to the DB # noqa: E501

#     :param id:
#     :type id: int
#     :param cpu_model:
#     :type cpu_model: str
#     :param cpu_cores:
#     :type cpu_cores: int
#     :param ram_capacity:
#     :type ram_capacity: str

#     :rtype: Metric
#     """
#     return 'do some magic!'


def delete_metric(metric_id):  # noqa: E501
    """Deletes a Metric

    delete a Metric # noqa: E501

    :param metric_id: Metric id to delete
    :type metric_id: int

    :rtype: None
    """
    global metrics
    new_metrics = []
    for metric in metrics:
        if metric["id"] == metric_id:
            continue
        new_metrics.append(metric)
    metrics = new_metrics


def get_all_metrics():  # noqa: E501
    """Get all metrics

    Get all metrics # noqa: E501


    :rtype: List[Metric]
    """
    global metrics
    return metrics


def get_metric_by_id(metric_id):  # noqa: E501
    """Find metric by ID

    Returns a single metric # noqa: E501

    :param metric_id: ID of metric to return
    :type metric_id: int

    :rtype: Metric
    """
    global metrics
    for metric in metrics:
        print(metric)
        if metric["id"] == metric_id:
            return metric
        return "", 404


def update_metric(body):  # noqa: E501
    """Update an existing metric

    Update an existing metric by Id # noqa: E501

    :param body: Update an existent metric in the DB
    :type body: dict | bytes

    :rtype: Metric
    """
    if connexion.request.is_json:
        body = Metric.from_dict(connexion.request.get_json())  # noqa: E501

    global metrics
    new_metrics = []
    payload = None
    for metric in metrics:
        if metric["id"] == body.id:
            payload = {
                "id": metric["id"],
                "cpu_model": body.cpu_model,
                "cpu_cores": body.cpu_cores,
                "ram_capacity": body.ram_capacity
            }
            new_metrics.append(payload)
        else:
            new_metrics.append(metric)
    metrics = new_metrics
    return payload


# def update_metric(id, cpu_model, cpu_cores, ram_capacity):  # noqa: E501
#     """Update an existing metric

#     Update an existing metric by Id # noqa: E501

#     :param id:
#     :type id: int
#     :param cpu_model:
#     :type cpu_model: str
#     :param cpu_cores:
#     :type cpu_cores: int
#     :param ram_capacity:
#     :type ram_capacity: str

#     :rtype: Metric
#     """
#     return 'do some magic!'


def update_metric_with_form(metric_id, cpu_model=None, cpu_cores=None, ram_capacity=None):  # noqa: E501
    """Updates a metric in the DB with form data

     # noqa: E501

    :param metric_id: ID of metric that needs to be updated
    :type metric_id: int
    :param cpu_model: Cpu Model of metric that needs to be updated
    :type cpu_model: str
    :param cpu_cores: Number of Cpu Cores of metric that needs to be updated
    :type cpu_cores: int
    :param ram_capacity: RAM Capacity of metric that needs to be updated
    :type ram_capacity: str

    :rtype: None
    """
    global metrics
    new_metrics = []
    payload = None
    for metric in metrics:
        if metric["id"] == metric_id:
            payload = {
                "id": metric["id"],
                "cpu_model": cpu_model,
                "cpu_cores": cpu_cores,
                "ram_capacity": ram_capacity
            }
            new_metrics.append(payload)
        else:
            new_metrics.append(metric)
    metrics = new_metrics
    return payload
