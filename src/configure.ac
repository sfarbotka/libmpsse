AC_PREREQ([2.65])
AC_INIT([libmpsse],[1.2],[http://libmpsse.googlecode.com])

AC_ARG_ENABLE([python],AS_HELP_STRING([--disable-python], [Do not build Python wrappers]))
AS_IF([test "x$enable_python" != "xno"], [BUILD="swig"], [BUILD=""])

AC_CONFIG_SRCDIR([mpsse.c])

AC_PROG_CC
AC_LANG(C)

AC_TYPE_SIZE_T
AC_FUNC_MALLOC

LDFLAGS="-lftdi $LDFLAGS"
CFLAGS="-Wall -fPIC -fno-strict-aliasing $CFLAGS"

AC_CHECK_FUNCS([malloc memset],[],AC_MSG_ERROR(["missing standard functions"]))
AC_CHECK_LIB([ftdi],[ftdi_init],[],[echo "error: missing libftdi library" && exit 1],[])
AC_CHECK_HEADERS([stdlib.h stdint.h string.h],[],[echo "error: missing standard header files" && exit 1])
AC_CHECK_HEADERS([ftdi.h],[],[echo "error: missing libftdi header files" && exit 1])

if test $BUILD
then
	if ! test $SWIG
	then
		SWIG="$(which swig)"
	fi

	if ! test $SWIG
	then
		echo "error: could not locate swig"
		exit 1
	fi

	if ! test $PYDEV
	then
		PYDEV="/usr/include/python$(python --version 2>&1 | awk '{print $2}' | cut -d'.' -f1,2)"
	fi

	AC_CHECK_HEADERS([$PYDEV/Python.h],[],[echo "error: missing python header files" && exit 1])

	if ! test $PYLIB
	then
		dnl This is a hack to get a valid python library path
		echo "import sys" > pylib.py
		echo "for path in sys.path: print path" >> pylib.py
		PYLIB="$(python pylib.py | grep -e '-packages$' | head -1)"
		rm -f pylib.py
	fi

	if ! test -d $PYLIB
	then
		echo "error: could not locate python library path"
		exit 1
	fi
fi

dnl OSX specific compiler flags
if test "$(uname)" == "Darwin"
then
	SONAME="-install_name"
	FRAMEWORK="-framework Python"
else
	SONAME="-soname"
	FRAMEWORK=""
fi

cp confdefs.h config.h

AC_SUBST(BUILD, $BUILD)
AC_SUBST(SWIG, $SWIG)
AC_SUBST(PYDEV, $PYDEV)
AC_SUBST(PYLIB, $PYLIB)
AC_SUBST(SONAME, $SONAME)
AC_SUBST(FRAMEWORK, $FRAMEWORK)
AC_CONFIG_FILES([Makefile])
AC_OUTPUT
