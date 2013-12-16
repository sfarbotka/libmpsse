AC_PREREQ([2.65])
AC_INIT([libmpsse],[1.2],[http://libmpsse.googlecode.com])
PKG_PROG_PKG_CONFIG(0.28)

AC_ARG_ENABLE([python],AS_HELP_STRING([--disable-python], [Do not build Python wrappers]))
AS_IF([test "x$enable_python" != "xno"], [BUILD="swig"], [BUILD=""])

AC_CONFIG_SRCDIR([mpsse.c])

AC_PROG_CC
AC_LANG(C)

AC_TYPE_SIZE_T
AC_FUNC_MALLOC

AC_CHECK_FUNCS([malloc memset],[],AC_MSG_ERROR(["missing standard functions"]))
AC_CHECK_HEADERS([stdlib.h stdint.h string.h],[],AC_MSG_ERROR(["error: missing standard header files"]))
PKG_CHECK_MODULES([FTDI1], [libftdi1 >= 1.0])

dnl For OSX add MacPorts paths
AS_IF([test "$(uname)" == "Darwin"],
[
    LDFLAGS="$LDFLAGS -L/opt/local/lib"
    CFLAGS="$CFLAGS -I/opt/local/include"
])

dnl AC_CHECK_HEADERS([ftdi.h],[],[echo "error: missing libftdi header files" && exit 1])
dnl AC_CHECK_LIB([ftdi1],[ftdi_init],[],[echo "error: missing libftdi library" && exit 1],[])

AS_IF([test $BUILD],
[
	AS_IF([! test $SWIG], [SWIG="$(which swig)"])
	AS_IF([! test $SWIG], [SWIG="$(which swig2.0)"])
	AS_IF([! test $SWIG], AC_MSG_ERROR(["error: could not locate swig"]))

	AS_IF([[[ "$(uname)" == MINGW*]]],
	[
		AS_IF([! test $PYTHON], [PYTHON="C:/Python27/python.exe"])
		AS_IF([! test $PYINCDIR], [PYINCDIR="C:/Python27/include"])
		AS_IF([! test $PYLIBDIR], [PYLIBDIR="C:/Python27/libs"])
		PYLDFLAGS="-lpython27 -L$PYLIBDIR"
		PYCFLAGS="-I$PYINCDIR"
		PYCPPFLAGS="-I$PYINCDIR"
	],
	[
		AS_IF([! test $PYTHON], [PYTHON="$(which python)"])
		AS_IF([! test $PYTHON], AC_MSG_ERROR(["error: python not found"]))
		AS_IF([! test $PYCONF], [PYCONF="$(which python-config)"])
		AS_IF([! test $PYCONF], AC_MSG_ERROR(["error: python-config not found"]))

		PYLDFLAGS="$($PYCONF --libs)"
		PYCFLAGS="$($PYCONF --includes)"
		PYCPPFLAGS="$($PYCONF --includes)"
	])

	LDFLAGS="$PYLDFLAGS $LDFLAGS"
	CFLAGS="$PYCFLAGS $CFLAGS"
	CPPFLAGS="$PYCPPFLAGS $CPPFLAGS"

	AC_CHECK_HEADERS([Python.h],[],AC_MSG_ERROR(["error: missing python header files"]))

	AS_IF([! test $PYLIB],
	[
		dnl This is a hack to get a valid python library path
		script=$(printf "import sys\nfor p in sys.path: print p")
		PYLIB=$($PYTHON -c "$script" | grep -e '-packages$' | head -1)
	])

	AS_IF([! test $PYLIB], AC_MSG_ERROR(["error: could not locate python site-packages path"]))
])

LDFLAGS="$LDFLAGS $FTDI1_LIBS"
CFLAGS="-Wall $FTDI1_CFLAGS $CFLAGS"

dnl system specific compiler flags
ISMINGW=0
AS_CASE([$(uname)], 
[MINGW*], 
[
 	ISMINGW=1
	SONAME="-soname"
	AS_IF([test $BUILD], [LIBEXT="pyd"], [LIBEXT="dll"])
],
[Darwin],
[
	SONAME="-install_name"
	LIBEXT="so"
],
[
	SONAME="-soname"
	LIBEXT="so"
])

cp confdefs.h config.h

AC_SUBST(BUILD, $BUILD)
AC_SUBST(SWIG, $SWIG)
AC_SUBST(PYLIB, $PYLIB)
AC_SUBST(SONAME, $SONAME)
AC_SUBST(LIBEXT, $LIBEXT)
AC_SUBST(TARGET, mpsse)
AC_SUBST(ISMINGW, $ISMINGW)
AC_CONFIG_FILES([Makefile examples/Makefile])
AC_OUTPUT
