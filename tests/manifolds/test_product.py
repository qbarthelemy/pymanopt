import numpy as np
import numpy.testing as np_testing

from pymanopt.manifolds import Euclidean, Grassmann, Product, Sphere

from .._test import TestCase


class TestProductManifold(TestCase):
    def setUp(self):
        self.m = m = 100
        self.n = n = 50
        self.euclidean = Euclidean(m, n)
        self.sphere = Sphere(n)
        self.manifold = Product([self.euclidean, self.sphere])

    def test_dim(self):
        np_testing.assert_equal(
            self.manifold.dim, self.m * self.n + self.n - 1
        )

    def test_typical_dist(self):
        np_testing.assert_equal(
            self.manifold.typical_dist, np.sqrt((self.m * self.n) + np.pi**2)
        )

    def test_dist(self):
        X = self.manifold.random_point()
        Y = self.manifold.random_point()
        np_testing.assert_equal(
            self.manifold.dist(X, Y),
            np.sqrt(
                self.euclidean.dist(X[0], Y[0]) ** 2
                + self.sphere.dist(X[1], Y[1]) ** 2
            ),
        )

    def test_tangent_vector_multiplication(self):
        # Regression test for https://github.com/pymanopt/pymanopt/issues/49.
        manifold = Product((Euclidean(12), Grassmann(12, 3)))
        x = manifold.random_point()
        eta = manifold.random_tangent_vector(x)
        np.float64(1.0) * eta

    # def test_inner_product(self):

    # def test_projection(self):

    # def test_euclidean_to_riemannian_hessian(self):

    # def test_retraction(self):

    # def test_euclidean_to_riemannian_gradient(self):

    # def test_norm(self):

    # def test_rand(self):

    # def test_random_tangent_vector(self):

    # def test_transport(self):

    def test_exp_log_inverse(self):
        s = self.manifold
        X = s.random_point()
        Y = s.random_point()
        Yexplog = s.exp(X, tangent_vector=s.log(X, Y))
        np_testing.assert_almost_equal(s.dist(point_a=Y, point_b=Yexplog), 0)

    def test_log_exp_inverse(self):
        s = self.manifold
        X = s.random_point()
        U = s.random_tangent_vector(X)
        Ulogexp = s.log(X, s.exp(X, U))
        np_testing.assert_array_almost_equal(U[0], Ulogexp[0])
        np_testing.assert_array_almost_equal(U[1], Ulogexp[1])

    def test_pair_mean(self):
        s = self.manifold
        X = s.random_point()
        Y = s.random_point()
        Z = s.pair_mean(X, Y)
        np_testing.assert_array_almost_equal(s.dist(X, Z), s.dist(Y, Z))
