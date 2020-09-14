#include <criterion/criterion.h>

#include "arithmetic.h"

Test(addition, add_two_positive_numbers)
{
    float x;

    x = add(5, 7);

    cr_assert_eq(x, 12);
}


Test(addition, add_two_negative_numbers)
{
    float x;

    x = add(-5, -7);

    cr_assert_eq(x, -12);
}


Test(addition, add_negative_and_positive_numbers_1)
{
    float x;

    x = add(5, -7);

    cr_assert_eq(x, -2);
}


Test(addition, add_negative_and_positive_numbers_2)
{
    float x;

    x = add(-5, 7);

    cr_assert_eq(x, 2);
}


Test(addition, add_zero)
{
    float x;

    x = add(100, 0);

    cr_assert_eq(x, 100);
}