import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient
from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_one_course(client, course_factory):

    # Arrange
    courses = course_factory(_quantity=1)

    # Act
    response = client.get('/courses/1/')
    data = response.json()

    # Assert
    assert response.status_code == 200

    for item in courses:
        assert item.id == data['id']


@pytest.mark.django_db
def test_get_courses_list(client, course_factory):

    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get('/courses/')
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert len(data) == len(courses)

    for i, value in enumerate(data):
        assert value['name'] == courses[i].name


@pytest.mark.django_db
def test_course_filter_id(client, course_factory):

    # Arrange
    courses = course_factory(_quantity=5)
    data = {'id': courses[0].id}

    # Act
    url = reverse('courses-list')
    response = client.get(url, data=data)
    response_server = response.json()

    # Assert
    assert response.status_code == 200
    assert data['id'] in [item['id'] for item in response_server]


@pytest.mark.django_db
def test_course_filter_name(client, course_factory):

    # Arrange
    courses = course_factory(_quantity=5)
    data = {'name': courses[0].name}

    # Act
    url = reverse('courses-list')
    response = client.get(url, data=data)
    response_server = response.json()

    # Assert
    assert response.status_code == 200
    assert data['name'] in [item['name'] for item in response_server]


@pytest.mark.django_db
def test_create_course(client):

    # Arrange
    count = Course.objects.count()

    # Act
    response = client.post('/courses/', data={'name': 'Ivan',},)

    # Assert
    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_patch_update_course(client, course_factory):

    # Arrange
    courses = course_factory(_quantity=5)

    # Act
    response_update = client.patch('/courses/1/', data={'name': 'Ivan',},)
    response_get = client.get('/courses/1/')
    response_update_format = response_update.json()
    response_get_format = response_get.json()

    # Assert
    assert response_update.status_code == 200
    assert response_update_format['id'] == response_get_format['id']


@pytest.mark.django_db
def test_put_update_course(client, course_factory):

    # Arrange
    courses = course_factory(_quantity=5)

    # Act
    response_update = client.put('/courses/1/', data={'name': 'Ivan',},)
    response_get = client.get('/courses/1/')
    response_update_format = response_update.json()
    response_get_format = response_get.json()

    # Assert
    assert response_update.status_code == 200
    assert response_update_format['id'] == response_get_format['id']


@pytest.mark.django_db
def test_delete_course(client, course_factory):

    # Arrange
    courses = course_factory(_quantity=5)
    count = Course.objects.count()

    # Act
    response = client.delete('/courses/1/',)

    # Assert
    assert response.status_code == 204
    assert Course.objects.count() == count - 1
