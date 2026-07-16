export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="wrap">
        <p className="wordmark" aria-hidden="true">
          NORVIA
        </p>
        <div className="foot-row">
          <span>© {new Date().getFullYear()} Norvia Solutions</span>
          <span>Feito com React, café e código limpo</span>
        </div>
      </div>
    </footer>
  )
}
