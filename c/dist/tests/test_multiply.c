#include <criterion/criterion.h>

#include "arithmetic.h"

Test(multiplication, multiply_two_positive_numbers)
{
    float x;

    x = multiply(5, 7);

    cr_assert_eq(x, 35);
}


Test(multiplication, multiply_two_negative_numbers)
{
    float x;

    x = multiply(-5, -7);

    cr_assert_eq(x, 35);
}


Test(multiplication, multiply_negative_and_positive_numbers)
{
    float x;

    x = multiply(5, -7);

    cr_assert_eq(x, -35);
}


Test(multiplication, multiply_one)
{
    float x;

    x = multiply(100, 1);

    cr_assert_eq(x, 100);
}


Test(multiplication, multiply_zero)
{
    float x;

    x = multiply(100, 0);

    cr_assert_eq(x, 0);
}