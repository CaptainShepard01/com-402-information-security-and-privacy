# Ex.1
(!flag.startsWith("MOBISEC{") ||
new StringBuilder(flag).reverse().toString().charAt(0) != '}' ||
flag.length() != 35 ||
!flag.toLowerCase().substring(8).startsWith("this_is_") ||
!new StringBuilder(flag).reverse().toString().toLowerCase().substring(1).startsWith(ctx.getString(R.string.last_part)) ||
flag.charAt(17) != '_' ||
flag.charAt((int) (getY() * Math.pow(getX(), getY()))) != flag.charAt(((int) Math.pow(Math.pow(2.0d, 2.0d), 2.0d)) + 1) ||
!bam(flag.toUpperCase().substring(getY() * getX() * getY(), (int) (Math.pow(getZ(), getX()) - 1.0d))).equals("ERNYYL") ||
flag.toLowerCase().charAt(16) != 'a' ||
flag.charAt(16) != flag.charAt(26) ||
flag.toUpperCase().charAt(25) != flag.toUpperCase().charAt(26) + 1)


MOBISEC{ThIs_iS_A_ReAlLy_bAsIc_rEv}
ver_cis

[A-Z_][a-z_][A-Z_][a-z_]...

flag.toUpperCase().substring(18, 24) = REALLY


# Ex.2

703958