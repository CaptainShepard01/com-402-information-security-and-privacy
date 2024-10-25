#include <stdio.h>

union options
{
  int option_a;
  float option_b;
};

int main() {
  union options o;

  // 1073741825
  printf("input value for option_a: ");
  scanf("%d", &o.option_a);

  printf("option_a %i\n", o.option_a);
  printf("option_b interpreted as %f\n", o.option_b);
}
