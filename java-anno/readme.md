# Java 配置
—— Java 注解配置，以替换 XML 配置文件。（注意，最终还是有 properties 配置文件的。）

示例：
```java
package cn.demo.config;

@Configuration
@ProperitySource("classpath:jdbc.properties")
public class JdbcConfig {
    @Value("${jdbc.url}")
    String url;
    @Value("${jdbc.driverClassName}")
    String driverClassName;
    @Value("${jdbc.username}")
    String username;
    @Value("${jdbc.password}")
    String password;

    @Bean
    public DataSource dataSource() {
        DruidDataSource dataSource = new DruidDataSource();
        dataSource.setDriverClassName(driverClassName);
        dataSource.setUrl(url);
        dataSource.setUsername(username);
        dataSource.setPassword(password);
        return dataSource;
    }
}
```

## SpringBoot 基于 Java 配置进一步引申扩展的配置方式

#### 1 创建 application.properties 文件
```
jdbc.url=""
jdbc.driverClassName=""
jdbc.username=""
jdbc.password=""
```

#### 2 创建 JdbcProperties 类
```java
package cn.demo.config;

import lombok.Data;  //用于自动生成 setter getter
import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "jdbc")
@Data
public class JdbcProperties {
    String url;
    String driverClassName;
    String username;
    String password;
}
```

#### 3 创建 JdbcConfig 注解类
```java
package cn.demo.config;

@Configuration
@EnableConfigurationProperties(JdbcProperties.class)
public class JdbcConfig {

    @Bean
    public DataSource dataSource(JdbcProperties prop) {
        DruidDataSource dataSource = new DruidDataSource();
        dataSource.setDriverClassName(prop.GetDriverClassName());
        dataSource.setUrl(prop.GetUrl());
        dataSource.setUsername(prop.GetUsername());
        dataSource.setPassword(prop.GetPassword());
        return dataSource;
    }
}
```

## 使用 ConfigurationProperties 对象的其他多种方式

#### 1 通过 Autowired 方式
```java
package cn.demo.config;

@Configuration
@EnableConfigurationProperties(JdbcProperties.class)
public class JdbcConfig {

    @Autowired
    JdbcProperties jdbcProperties;

    @Bean
    public DataSource dataSource() {
        DruidDataSource dataSource = new DruidDataSource();
        dataSource.setDriverClassName(jdbcProperties.GetDriverClassName());
        dataSource.setUrl(jdbcProperties.GetUrl());
        dataSource.setUsername(jdbcProperties.GetUsername());
        dataSource.setPassword(jdbcProperties.GetPassword());
        return dataSource;
    }
}
```

#### 2 通过构造函数方式
```java
package cn.demo.config;

@Configuration
@EnableConfigurationProperties(JdbcProperties.class)
public class JdbcConfig {

    JdbcProperties jdbcProperties;

    public JdbcConfig(JdbcProperties jdbcProperties) {
        this.jdbcProperties = jdbcProperties;
    }

    @Bean
    public DataSource dataSource() {
        DruidDataSource dataSource = new DruidDataSource();
        dataSource.setDriverClassName(jdbcProperties.GetDriverClassName());
        dataSource.setUrl(jdbcProperties.GetUrl());
        dataSource.setUsername(jdbcProperties.GetUsername());
        dataSource.setPassword(jdbcProperties.GetPassword());
        return dataSource;
    }
}
```

## 