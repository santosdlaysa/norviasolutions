import { Link } from 'react-router-dom'
import Reveal from '../components/Reveal'
import { PRODUCTS, SOCIALS, CONTACT_EMAIL } from '../data/products'

export default function Home() {
  return (
    <main>
      <section className="hero wrap">
        <p className="eyebrow">Estúdio de software · Brasil</p>
        <h1>
          Software que resolve o dia a dia de <em>negócios reais</em>.
        </h1>
        <p className="lead">
          A Norvia Solutions cria aplicativos e sistemas web para quem produz, vende e atende: da
          confeitaria à lavoura, da cafeteria à agenda lotada. Produto próprio, do design ao deploy.
        </p>
        <div className="hero-ctas">
          <a className="btn btn-gold" href="#produtos">
            Conheça os produtos
          </a>
          <a className="btn btn-ghost" href="#contato">
            Fale com a gente
          </a>
        </div>
        <div className="hero-meta">
          <span>
            <strong>{PRODUCTS.length}+</strong> produtos lançados
          </span>
          <span>
            <strong>iOS · Android · Web</strong>
          </span>
          <span>React · React Native · Flutter · TypeScript</span>
        </div>
      </section>

      <section className="block" id="produtos">
        <div className="wrap">
          <Reveal className="sec-head">
            <div>
              <p className="eyebrow">Portfólio</p>
              <h2 className="sec-title">Produtos feitos aqui dentro</h2>
            </div>
            <p>
              Cada produto nasceu de um problema concreto — precificar, plantar, agendar, organizar
              — e está em produção, nas lojas ou na web.
            </p>
          </Reveal>
          <div className="grid">
            {PRODUCTS.map((p) => (
              <Reveal key={p.slug} style={{ display: 'grid' }}>
                <Link
                  className="card"
                  style={{ '--hue': p.hue } as React.CSSProperties}
                  to={`/produtos/${p.slug}`}
                >
                  <span className="tag">{p.tag}</span>
                  <h3>{p.name}</h3>
                  <p>{p.summary}</p>
                  <span className="foot">
                    <span>
                      {p.platform} · {p.tech.split(' · ')[0]}
                    </span>
                    <span className="go">Detalhes ↗</span>
                  </span>
                </Link>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="block" id="servicos">
        <div className="wrap">
          <Reveal className="sec-head">
            <div>
              <p className="eyebrow">Serviços</p>
              <h2 className="sec-title">O que construímos para você</h2>
            </div>
            <p>
              A mesma engenharia dos nossos produtos, aplicada ao seu negócio — do primeiro rascunho
              à publicação nas lojas.
            </p>
          </Reveal>
          <Reveal>
            <div className="servicos">
              <div className="servico">
                <span className="num">Mobile</span>
                <h3>Aplicativos iOS &amp; Android</h3>
                <p>
                  Apps nativos de verdade com React Native e Flutter, publicados na App Store e no
                  Google Play — como o Orgenyx e o Doce Preço.
                </p>
              </div>
              <div className="servico">
                <span className="num">Web</span>
                <h3>Sistemas de gestão</h3>
                <p>
                  Sistemas web sob medida para controlar vendas, estoque, agendamentos e produção,
                  acessíveis de qualquer dispositivo.
                </p>
              </div>
              <div className="servico">
                <span className="num">Presença</span>
                <h3>Sites &amp; landing pages</h3>
                <p>
                  Páginas rápidas e responsivas que apresentam seu negócio e convertem visitantes em
                  clientes.
                </p>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      <section className="block" id="sobre">
        <div className="wrap sobre-grid">
          <Reveal className="txt">
            <p className="eyebrow">Sobre a Norvia</p>
            <h2 className="sec-title">Um estúdio pequeno com produtos grandes</h2>
            <p>
              A Norvia Solutions nasceu do portfólio de <strong>Laysa Diniz</strong>, desenvolvedora
              fullstack que transformou uma sequência de produtos próprios — apps nas lojas,
              sistemas em produção — em um estúdio de software.
            </p>
            <p>
              Trabalhamos com <strong>React, React Native, Flutter e TypeScript</strong>, cuidando
              de todo o ciclo: descoberta do problema, design da interface, desenvolvimento,
              publicação e evolução contínua.
            </p>
            <p>
              Se os nossos produtos resolvem o dia a dia de confeiteiras, produtores e prestadores
              de serviço, o seu problema também tem solução.
            </p>
          </Reveal>
          <Reveal className="valores">
            <div className="valor">
              <span className="mark">→</span>
              <div>
                <h4>Produto antes de código</h4>
                <p>Entendemos o negócio primeiro; a tecnologia vem a serviço dele.</p>
              </div>
            </div>
            <div className="valor">
              <span className="mark">→</span>
              <div>
                <h4>Entrega de ponta a ponta</h4>
                <p>Do rascunho à loja de aplicativos, sem intermediários.</p>
              </div>
            </div>
            <div className="valor">
              <span className="mark">→</span>
              <div>
                <h4>Simples de usar</h4>
                <p>Interfaces que qualquer pessoa opera sem manual.</p>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      <section className="block" id="contato">
        <div className="wrap">
          <Reveal>
            <div className="contato-box">
              <p className="eyebrow">Contato</p>
              <h2>Tem um problema que software resolve?</h2>
              <p>
                Conte pra gente o que trava o seu dia a dia. A Norvia transforma isso em um app ou
                sistema que funciona.
              </p>
              <a className="btn btn-gold" href={`mailto:${CONTACT_EMAIL}`}>
                {CONTACT_EMAIL}
              </a>
              <div className="socials">
                {SOCIALS.map((s) => (
                  <a key={s.label} href={s.url} target="_blank" rel="noopener noreferrer">
                    {s.label} ↗
                  </a>
                ))}
              </div>
            </div>
          </Reveal>
        </div>
      </section>
    </main>
  )
}
