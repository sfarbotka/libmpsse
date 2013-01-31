AC_PREREQ([2.65])
AC_INIT([libmpsse],[1.2],[http://libmpsse.googlecode.com])

AC_ARG_ENABLE([python],AS_HELP_STRING([--disable-python], [Do not build Python wrappers]))
AS_IF([test "x$enable_python" != "xno"], [BUILD="swig"], [BUILD=""])

AC_CONFIG_SRCDIR([mpsse.c])

AC_PROG_CC
AC_LANG(C)

AC_TYPE_SIZE_T
AC_FUNC_MALLOC

AC_CHECK_FUNCS([malloc memset],[],AC_MSG_ERROR(["missing standard functions"]))
AC_CHECK_HEADERS([stdlib.h stdint.h string.h],[],AC_MSG_ERROR(["error: missing standard header files"]))

dnl For OSX add MacPorts paths
AS_IF([test "$(uname)" == "Darwin"],
[
    LDFLAGS="$LDFLAGS -L/opt/local/lib"
    CFLAGS="$CFLAGS -I/opt/local/include"
])

AC_CHECK_HEADERS([ftdi.h],[],[echo "error: missing libftdi header files" && exit 1])
AC_CHECK_LIB([ftdi],[ftdi_init],[],[echo "error: missing libftdi library" && exit 1],[])

if test $BUILD
then
	AS_IF([! test $SWIG], [SWIG="$(which swig)"])
	AS_IF([! test $SWIG], [SWIG="$(which swig2.0)"])
	AS_IF([! test $SWIG], AC_MSG_ERROR(["error: could not locate swig"]))

	if [[[ "$(uname)" == MINGW* ]]] ; then
		AS_IF([! test $PYTHON], [PYTHON="C:\Python27\python.exe"])
		AS_IF([! test $PYINCDIR], [PYINCDIR="C:\Python27\include"])
		AS_IF([! test $PYLIBDIR], [PYLIBDIR="C:\Python27\libs"])
		PYLDFLAGS="-lpython27 -L$PYLIBDIR"
		PYCFLAGS="-I$PYINCDIR"
	else
		AS_IF([! test $PYTHON], [PYTHON="$(which python)"])
		AS_IF([! test $PYTHON], AC_MSG_ERROR(["error: python not found"]))
		AS_IF([! test $PYCONF], [PYCONF="$(which python-config)"])
		AS_IF([! test $PYCONF], AC_MSG_ERROR(["error: python-config not found"]))

		PYLDFLAGS="$($PYCONF --libs)"
		PYCFLAGS="$($PYCONF --includes)"
	fi

	LDFLAGS="$PYLDFLAGS $LDFLAGS"
	CFLAGS="$PYCFLAGS $CFLAGS"

	AC_CHECK_HEADERS([Python.h],[],[echo "error: missing python header files" && exit 1])

	if ! test $PYLIB
	then
		dnl This is a hack to get a valid python library path
		script=$(printf "import sys\nfor p in sys.path: print p")
		PYLIB=$($PYTHON -c "$script" | grep -e '-packages$' | head -1)
	fi

	AS_IF([! test $PYLIB], AC_MSG_ERROR(["error: could not locate python site-packages path"]))
fi

LDFLAGS="-lftdi $LDFLAGS"
CFLAGS="-Wall -fPIC -fno-strict-aliasing $CFLAGS"

dnl system specific compiler flags
AS_CASE([$(uname)], 
[MINGW*], 
[
	SONAME="-soname"
	LIBEXT="pyd"
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
AC_CONFIG_FILES([Makefile])
AC_OUTPUT
