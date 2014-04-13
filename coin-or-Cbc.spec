%global		_disable_ld_no_undefined	1
%global		module		Cbc

Name:		coin-or-%{module}

Summary:	Coin-or branch and cut
Version:	2.8.9
Release:	1%{?dist}
License:	EPL
URL:		http://projects.coin-or.org/%{module}
Source0:	http://www.coin-or.org/download/pkgsource/%{module}/%{module}-%{version}.tgz
Source1:	%{name}.rpmlintrc
BuildRequires:	blas-devel
BuildRequires:	bzip2-devel
BuildRequires:	coin-or-Clp-devel
BuildRequires:	coin-or-Cgl-devel
BuildRequires:	coin-or-CoinUtils-devel
BuildRequires:	coin-or-Osi-devel
BuildRequires:	doxygen
BuildRequires:	glpk-devel
BuildRequires:	graphviz
BuildRequires:	lapack-devel
BuildRequires:	libatlas-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	zlib-devel

# Properly handle DESTDIR
Patch0:		%{name}-pkgconfig.patch

# Install documentation in standard rpm directory
Patch1:		%{name}-docdir.patch

# Avoid empty #define if svnversion is available at configure time
Patch2:		%{name}-svnversion.patch

%description
Cbc (Coin-or branch and cut) is an open-source mixed integer programming
solver written in C++. It can be used as a callable library or using a
stand-alone executable. It can be called through AMPL (natively), GAMS
(using the links provided by the "Optimization Services" and "GAMSlinks"
projects), MPL (through the "CoinMP" project), AIMMS (through the "AIMMSlinks"
project), or "PuLP".

Cbc links to a number of other COIN projects for additional functionality,
including:

   * Clp (the default solver for LP relaxations)
   * Cgl (for cut generation)
   * CoinUtils (for reading input files and various utilities)

%package	devel
Summary:	Development files for %{name}

Requires:	coin-or-CoinUtils-devel
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	doc
Summary:	Documentation files for %{name}

Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
This package contains the documentation for %{name}.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# silence doxygen deprecation warnings
sed -i 's/^\(SYMBOL_CACHE_SIZE\|SHOW_DIRECTORIES\|HTML_ALIGN_MEMBERS\|USE_INLINE_TREES\|DOT_FONTNAME\)/#\1/g' doxydoc/doxygen.conf.in

%build
mkdir bin; pushd bin; ln -sf %{_bindir}/ld.bfd ld; popd; export PATH=$PWD/bin:$PATH
CFLAGS="%{optflags} -fuse-ld=bfd" CXXFLAGS="%{optflags} -fuse-ld=bfd" \
%configure2_5x
# Kill rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags} all doxydoc

%install
export PATH=$PWD/bin:$PATH
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la
cp -a doxydoc/html %{buildroot}%{_docdir}/%{name}

%check
export PATH=$PWD/bin:$PATH
LD_LIBRARY_PATH=%{buildroot}%{_libdir} make test

%files
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/AUTHORS
%doc %{_docdir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README
%doc %{_docdir}/%{name}/cbc_addlibs.txt
%{_bindir}/cbc
%{_libdir}/*.so.*

%files		devel
%{_includedir}/coin/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files		doc
%doc %{_docdir}/%{name}/html

%changelog
* Fri Mar 28 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.8.9-1
- Update to latest upstream release.

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.8.5-1
- Update to latest upstream release.

* Mon Jan 14 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.7.7-4
- Update to run make check (#894610#c4).

* Sat Jan 12 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.7.7-3
- Rename repackaged tarball.

* Sun Nov 18 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.7.7-2
- Rename package to coin-or-Cbc.
- Do not package Thirdy party data or data without clean license.

* Thu Sep 27 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.7.7-1
- Initial coinor-Cbc spec.
